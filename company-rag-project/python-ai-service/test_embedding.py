
from sentence_transformers import SentenceTransformer

# Load AI embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Sample text
text = "Employees can take 20 days of paid leave every year."

# Convert text into vector
vector = model.encode(text)

# Display results
print("Original Text:", text)
print("Total Vector Values:", len(vector))
print("First 10 Values:", vector[:10])
