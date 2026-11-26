package com.companyrag.company_rag_backend.service;

import java.util.Map;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service 
public class PythonAiService {
     private final RestClient pythonAiRestClient;

    public PythonAiService(RestClient pythonAiRestClient) {
        this.pythonAiRestClient = pythonAiRestClient;
    }

    public Map searchDocuments(String question, int topK) {

        Map<String, Object> request = Map.of(
                "question", question,
                "top_k", topK
        );

        return pythonAiRestClient.post()
                .uri("/api/ai/search")
                .body(request)
                .retrieve()
                .body(Map.class);
    }
}
