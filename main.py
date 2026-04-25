import os
import uuid
import numpy as np
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import chromadb
from collections import Counter
from openai import OpenAI
import json
from contextlib import asynccontextmanager # <--- Add this import
from fpdf import FPDF
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
load_dotenv()

# Create a folder to store the PDFs.
DOCS_OUTPUT_DIR = "generated_docs"
os.makedirs(DOCS_OUTPUT_DIR, exist_ok=True)


# --- 1. DEFINE THE LIFESPAN ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This part runs BEFORE the server starts (The "Birth")
    print("InnoGuard AI is starting up...")
    run_background_ingestion() 
    
    yield # <--- This is the "Pause" button. The app runs while it stays here.
    
    # This part runs when you SHUT DOWN the server (The "Death")
    print("InnoGuard AI is shutting down... Cleaning up.")

# --- 2. INITIALIZE FASTAPI WITH LIFESPAN ---
app = FastAPI(title="InnoGuard AI Backend", lifespan=lifespan)
# Tell FastAPI to serve files from this folder at the URL /download
app.mount("/download", StaticFiles(directory=DOCS_OUTPUT_DIR), name="download")

# --- 4. CONFIGURATION & CLIENTS ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ZAI_API_KEY = os.getenv("ZAI_API_KEY")

if not OPENAI_API_KEY or not ZAI_API_KEY:
    raise ValueError("Missing API Keys! Please check your .env file.")

# --- 1. CONFIGURATION & CLIENTS ---
# Using OpenAI for embeddings as per your tech stack
client_embeddings = OpenAI(api_key=OPENAI_API_KEY) 

# Using Z.AI GLM (ILMU) for Logic - Configured as per your Guide Book
# The guide says it's Anthropic-compatible via api.ilmu.ai
zai_client = OpenAI(
    base_url="https://api.ilmu.ai/v1", 
    api_key=ZAI_API_KEY,
    timeout=600.0
)

# Initialize Vector DB (Local)
chroma_client = chromadb.PersistentClient(path="./innoguard_db")
collection = chroma_client.get_or_create_collection(name="patent_collection")

# --- 2. MODELS ---
class IdeaRequest(BaseModel):
    category: str
    focus_area: str

class EvaluateRequest(BaseModel):
    title: str
    description: str
    tech_specs: str

class DocRequest(BaseModel):
    final_idea: str
    user_name: str
    doc_type: str = "patent"
    NDA_optional: Optional[str] = "NDA_FORM"

DISTANCE_THRESHOLD = 0.5 

def generate_cluster_label(titles: list):
    """
    Calls the Z.AI GLM to generate a professional 3-word label 
    based on patent titles in a group.
    """
    # Join titles into a numbered list for the prompt
    titles_context = "\n".join([f"- {t}" for t in titles])
    
    prompt = (
        "You are an Intellectual Property expert. "
        "I have a group of patents with the following titles:\n"
        f"{titles_context}\n\n"
        "What is a professional 3-word industry name for this sub-group? "
        "Return ONLY the 3 words."
    )
    try:
        response = zai_client.chat.completions.create(
            model="ilmu-glm-5.1",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"GLM Labeling failed: {e}")
        return "Specialized Technology" # Fallback if API fails

def run_background_ingestion():
    dummy_patents = [
    {
        "title": "Thermally Regulated Multi-Layer Composite Packaging",
        "text": (
            "A thermal insulation system for perishable goods delivery utilizing "
            "vacuum-sealed panels (VIP) integrated with bio-based phase-change materials (PCM). "
            "The implementation uses a core of fumed silica encapsulated in a barrier film of "
            "recycled polyethylene. The system maintains a constant internal temperature of 2-8°C "
            "for 48 hours without active power, specifically designed for pharmaceutical and high-end F&B."
        ),
        "cat": "F&B Delivery",
        "tech": "Vacuum Insulation, Phase-Change Materials, Fumed Silica"
    },
    {
        "title": "Wireless Induction Heating System for Portable Food Containers",
        "text": (
            "An active heating apparatus for insulated delivery bags. The system comprises a "
            "flexible copper induction coil array embedded in the base of the bag, powered by a "
            "detachable 20,000mAh Lithium-Polymer battery. It utilizes a resonant frequency "
            "inverter (100kHz) to trigger eddy currents in ferromagnetic inserts located within "
            "user-specific containers, allowing for localized heating up to 75°C."
        ),
        "cat": "F&B Delivery",
        "tech": "Induction Coils, Resonant Inverters, Li-Po Power Management"
    },
    {
        "title": "Shock-Absorbent Mycelium-Based Cargo Cushioning",
        "text": (
            "An eco-friendly alternative to expanded polystyrene (EPS) for logistics. "
            "The material is grown from fungal mycelium (Ganoderma lucidum) on a substrate "
            "of agricultural waste (hemp hurds). The implementation involves a cold-press "
            "molding process to create a cellular structure with high compressive strength "
            "and natural flame retardancy, designed for high-impact protection of electronic hardware."
        ),
        "cat": "Logistics",
        "tech": "Bio-Composite Manufacturing, Mycelium Growth, Compressive Testing"
    },
    {
        "title": "IoT-Enabled Smart Latching for Secure Parcel Lockers",
        "text": (
            "A cryptographic locking mechanism for last-mile delivery. The device uses an "
            "ESP32-based microcontroller with integrated 128-bit AES encryption. Access is granted "
            "via a dynamic QR code generated through a secure blockchain-based ledger. The hardware "
            "includes a high-torque 12V DC solenoid actuator and a proximity sensor to detect "
            "package placement before engaging the mechanical latch."
        ),
        "cat": "Logistics",
        "tech": "Microcontrollers, AES Encryption, Solenoid Actuators"
    },
    {
        "title": "Hydrophobic Nanocoatings for Moisture-Sensitive Food Packaging",
        "text": (
            "A chemical vapor deposition (CVD) process to apply a nanostructured silica (SiO2) "
            "layer onto cardboard surfaces. This creates a super-hydrophobic contact angle of >150 degrees, "
            "preventing structural degradation of the packaging when exposed to condensation in cold-chain "
            "delivery environments. The coating is FDA-approved for food contact and fully biodegradable."
        ),
        "cat": "F&B Delivery",
        "tech": "Nanotechnology, Chemical Vapor Deposition, Hydrophobic Polymers"
    }
    ] # Your detailed list from earlier

    for p in dummy_patents:
        # 1. Get Embedding for the new patent
        input_text = f"Title: {p['title']}. Description: {p['text']}"
        res = client_embeddings.embeddings.create(input=input_text, model="text-embedding-3-small")
        new_vector = res.data[0].embedding

        # 2. Check against the existing Database
        all_data = collection.get(include=['embeddings', 'metadatas'])
        
        assigned_group = None
        label = None
        
        if len(all_data['embeddings']) > 0:
            existing_vectors = np.array(all_data['embeddings'])
            similarities = np.dot(existing_vectors, new_vector)
            max_similarity = np.max(similarities)

            # --- LOGIC: CREATE NEW GROUP ---
            if max_similarity < (1 - DISTANCE_THRESHOLD):
                assigned_group = f"group_{uuid.uuid4().hex[:5]}"
                # Use GLM to label this brand new category
                # Since it's the first one, we name the group based on its title
                label = generate_cluster_label([p['title']])
                print(f"NEW GROUP DETECTED: Named it '{label}'")
            
            # --- LOGIC: JOIN EXISTING GROUP ---
            else:
                most_similar_index = np.argmax(similarities)
                assigned_group = all_data['metadatas'][most_similar_index]['sub_group']
                # Join existing group: inherit the label already created by GLM
                label = all_data['metadatas'][most_similar_index]['sub_group_label']
                print(f"Joining existing group: '{label}'")
        
        else:
            # First patent ever in the DB
            assigned_group = "group_initial"
            label = generate_cluster_label([p['title']])

        # 3. Save to ChromaDB
        collection.add(
            embeddings=[new_vector],
            documents=[p["text"]],
            metadatas=[{
                "category": p["cat"], 
                "title": p["title"], 
                "sub_group": assigned_group,
                "sub_group_label": label,
                "tech_used": p["tech"]
            }],
            ids=[str(uuid.uuid4())]
        )


# --- 4. API ENDPOINTS ---

@app.get("/")
def root():
    return {"message": "InnoGuard AI API is live"}


@app.post("/api/v1/generate-idea")
async def generate_idea(req: IdeaRequest):
    # 1. FETCH DATA FOR THE SELECTED CATEGORY
    # We ask ChromaDB for everything matching the user's category
    category_data = collection.get(
        where={"category": req.category},
        include=['metadatas', 'documents']
    )

    if not category_data['metadatas']:
        raise HTTPException(status_code=404, detail="No patent data found for this category.")

    # 2. FIND THE WHITESPACE (Sub-group with MINIMUM count)
    # Get all sub_groups in this category
    groups = [m['sub_group'] for m in category_data['metadatas']]
    group_counts = Counter(groups) # Returns something like {'group_1': 10, 'group_2': 2}
    
    # Find the ID of the group with the fewest patents
    whitespace_id = min(group_counts, key=group_counts.get)
    
    # Find the human-readable label for that whitespace
    # We just look at the metadata of the first item we find in that group
    whitespace_label = next(
        m['sub_group_label'] for m in category_data['metadatas'] 
        if m['sub_group'] == whitespace_id
    )
    existing_patents = [
        doc for doc, meta in zip(category_data['documents'], category_data['metadatas'])
        if meta['sub_group'] == whitespace_id
    ]
    context_text = "\n".join([f"- {p}" for p in existing_patents])
    # 3. GLM PROMPT 1: CREATIVE GENERATION
    # We combine the Industry + Whitespace + User's Focus Area
    creative_prompt = (
        f"Role: Expert Patent Strategist\n"
        f"Industry: {req.category}\n"
        f"Under-served Market (Whitespace): {whitespace_label}\n"
        f"User's Specific Focus: {req.focus_area}\n\n"
        f"EXISTING PATENTS IN THIS WHITESPACE TO AVOID:\n{context_text}\n\n"
        "Task: Suggest a unique, highly technical product idea that fits this whitespace. "
        "Return the response in this format:\n"
        "Title: [Name]\n"
        "Description: [2 sentences]\n"
        "Technical Innovation: [What makes it unique?]"
        "Return ONLY a JSON object with the keys: 'title', 'description', and 'technical_innovation'."
    )

    #res1 = zai_client.chat.completions.create(
    #    model="ilmu-glm-5.1",
    #    messages=[{"role": "user", "content": creative_prompt}]
    #)
    res1 = client_embeddings.chat.completions.create(
                model="gpt-4o-mini", # Reliable and fast
                messages=[{"role": "user", "content": creative_prompt}],
                response_format={ "type": "json_object" }
            )
    draft_content = json.loads(res1.choices[0].message.content)
    draft_text_for_embedding = f"{draft_content['title']}. {draft_content['description']} {draft_content['technical_innovation']}"
    # 4. INTERNAL LOOP (VERIFICATION)
    # Convert the draft into a vector to check if it's ACTUALLY unique
    emb_res = client_embeddings.embeddings.create(input=draft_text_for_embedding, model="text-embedding-3-small")
    search_res = collection.query(
        query_embeddings=[emb_res.data[0].embedding], 
        n_results=1
    )
    
    top_match_text = search_res['documents'][0][0]
    # Simple similarity calculation (1 - distance)
    distance = search_res['distances'][0][0]
    similarity_score = round((1 - distance) * 100, 2)

    # 5. GLM PROMPT 2: REFINEMENT (The "Self-Correction" Intelligence)
    final_idea = draft_content
    if similarity_score > 50: # If it's too similar to an existing patent
        refinement_prompt = (
            f"Your suggested idea: {json.dumps(draft_content)}\n\n"
            f"CRITIQUE: This idea is {similarity_score}% similar to an existing patent: '{top_match_text}'.\n"
            f"TASK: Modify the technical specs of your idea to avoid infringement while keeping the focus on {req.focus_area}. "
            "Ensure the final version is distinct. Return the same Title/Description/Innovation format."
            "Return the response in this format:\n"
            "Title: [Name]\n"
            "Description: [2 sentences]\n"
            "Technical Innovation: [What makes it unique?]"
            "Return ONLY a JSON object with the keys: 'title', 'description', and 'technical_innovation'."
        )
        #res2 = zai_client.chat.completions.create(
        #    model="ilmu-glm-5.1",
         #   messages=[{"role": "user", "content": refinement_prompt}]
        #)
        res2 = client_embeddings.chat.completions.create(
                model="gpt-4o-mini", # Reliable and fast
                messages=[{"role": "user", "content": refinement_prompt}],
                response_format={ "type": "json_object" }
            )
        final_idea = json.loads(res2.choices[0].message.content)

    # 6. RETURN CLEAN DATA
    # FIX: We deleted the manual string parsing (lines.split('\n')) because 'final_idea' is already a clean JSON dictionary!
    return {
        "status": "success",
        "whitespace_found": whitespace_label,
        "idea": final_idea,
        "verification": f"Optimization loop applied. Previous similarity was {similarity_score}%." if similarity_score > 50 else f"First draft highly unique. Highest similarity match was only {similarity_score}%."
    }


@app.post("/api/v1/evaluate-idea")
async def evaluate_idea(req: EvaluateRequest):
    # 1. VECTOR SEARCH: Find top 3 most similar patents
    emb_res = client_embeddings.embeddings.create(input=req.description, model="text-embedding-3-small")
    query_vector = emb_res.data[0].embedding
    
    search_res = collection.query(
        query_embeddings=[query_vector], 
        n_results=3,
        include=['documents', 'metadatas', 'distances']
    )
    
    # 2. PREPARE CONTEXT FOR GLM
    # We build a string that lists the patents found so the GLM can compare them
    similar_patents_context = ""
    similar_patents_list = []
    
    for i in range(len(search_res['documents'][0])):
        doc = search_res['documents'][0][i]
        meta = search_res['metadatas'][0][i]
        dist = search_res['distances'][0][i]
        similarity = round((1 - dist) * 100, 2)
        
        patent_info = {
            "id": f"MY-{i+100}", # In real life, use meta['id']
            "title": meta['title'],
            "similarity": f"{similarity}%",
            "owner": meta.get('owner', 'Unknown Entity'),
            "description": doc
        }
        similar_patents_list.append(patent_info)
        similar_patents_context += f"\nPATENT {i+1}:\nTitle: {meta['title']}\nDescription: {doc}\n"

    # 3. ADVANCED PROMPT: Comparison & Analysis
    prompt = (
        f"Role: Senior Patent Examiner\n"
        f"User's Invention Title: {req.title}\n"
        f"User's Tech Specs: {req.tech_specs}\n"
        f"User's Description: {req.description}\n\n"
        f"Existing Patents Found in Database:{similar_patents_context}\n\n"
        "Task: Perform a deep infringement risk analysis. Return ONLY a JSON object with this structure:\n"
        "{\n"
        "  'risk_score': (0-100 integer),\n"
        "  'verdict': (Short string),\n"
        "  'reasoning': (Why does it overlap?),\n"
        "  'closest_patent_title': (Which one is most dangerous?),\n"
        "  'pivots': [(List of 2 specific technical changes to avoid infringement)],\n"
        "  'patent_type': ('Standard Patent' if high novelty, 'Utility Innovation' if incremental improvement)\n"
        "}"
    )
    
    # 4. CALL GLM
    #res = zai_client.chat.completions.create(
     #   model="ilmu-glm-5.1",
     #   messages=[{"role": "user", "content": prompt}]
    #)
    res = client_embeddings.chat.completions.create(
                model="gpt-4o-mini", # Reliable and fast
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
    # Parse the GLM response
    analysis = json.loads(res.choices[0].message.content)
    
    # 5. RETURN COMBINED DATA
    return {
        "risk_assessment": {
            "risk_score": analysis.get("risk_score"),
            "verdict": analysis.get("verdict"),
            "reasoning": analysis.get("reasoning"),
            "closest_match": analysis.get("closest_patent_title")
        },
        "recommendation": {
            "patent_type": analysis.get("patent_type"),
            "pivots": analysis.get("pivots")
        },
        "similar_patents": similar_patents_list # These come directly from your ChromaDB
    }

@app.post("/api/v1/generate-docs")
async def generate_docs(req: DocRequest, request: Request):
    # --- 1. GLM LOGIC: DRAFT THE PATENT CONTENT ---
    patent_prompt = (
        f"You are a Malaysian Intellectual Property Lawyer. "
        f"Draft the 'Technical Description' and 'Claims' sections for a MyIPO Utility Innovation Form (Form P1) "
        f"for the invention: {req.final_idea}. "
        "Use highly formal, technical, and legal language. "
        "Structure it with clear headings for 'Description' and 'Claims'."
    )
    
   # res_patent = zai_client.chat.completions.create(
    #    model="ilmu-glm-5.1",
     #   messages=[{"role": "user", "content": patent_prompt}]
   # )
    res_patent = client_embeddings.chat.completions.create(
                model="gpt-4o-mini", # Reliable and fast
                messages=[{"role": "user", "content": patent_prompt}]
            )
    patent_content = res_patent.choices[0].message.content

    # --- 2. GLM LOGIC: DRAFT THE NDA ---
    nda_prompt = (
        f"Draft a standard legal Non-Disclosure Agreement (NDA) between {req.user_name} "
        f"and an undisclosed 'Manufacturer' regarding the product '{req.final_idea}'. "
        "Include standard clauses for Confidentiality, Duration (5 years), and Governing Law (Malaysia)."
    )
    
    #res_nda = zai_client.chat.completions.create(
     #   model="ilmu-glm-5.1",
      #  messages=[{"role": "user", "content": nda_prompt}]
   # )
    res_nda = client_embeddings.chat.completions.create(
                model="gpt-4o-mini", # Reliable and fast
                messages=[{"role": "user", "content": nda_prompt}]
            )
    nda_content = res_nda.choices[0].message.content

    # --- 3. PDF GENERATION LOGIC ---
    def create_pdf(filename, title, body):
        pdf = FPDF()
        pdf.add_page()
        # Add a Header
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, title, ln=True, align='C')
        pdf.ln(10)
        # Add the Content
        pdf.set_font("helvetica", "", 11)
        safe_body = body.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, safe_body)
        
        file_path = os.path.join(DOCS_OUTPUT_DIR, filename)
        pdf.output(file_path)
        return filename

    # Generate the unique filenames
    patent_filename = f"MyIPO_{uuid.uuid4().hex[:5]}.pdf"
    nda_filename = f"NDA_{uuid.uuid4().hex[:5]}.pdf"

    create_pdf(patent_filename, "MyIPO Utility Innovation Draft", patent_content)
    create_pdf(nda_filename, "Non-Disclosure Agreement", nda_content)

    # --- 4. RETURN THE REAL DOWNLOAD LINKS ---
    # Assuming your server runs on localhost:8000
    server_url = str(request.base_url).rstrip('/') 
    base_url = f"{server_url}/download" 
    
    return {
        "status": "documents_generated",
        "user": req.user_name,
        "files": {
            "patent_form_url": f"{base_url}/{patent_filename}",
            "nda_url": f"{base_url}/{nda_filename}"
        },
        "preview": {
            "patent_snippet": patent_content[:300] + "...",
            "nda_snippet": nda_content[:300] + "..."
        }
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
