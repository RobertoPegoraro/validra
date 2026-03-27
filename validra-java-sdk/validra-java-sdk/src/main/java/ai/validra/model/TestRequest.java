package ai.validra.model;

import java.util.Map;

public class TestRequest {

    private String endpoint;
    private String method;
    private Map<String, Object> examplePayload;
    private String type = "fuzz";

    // getters & setters
    public String getEndpoint() { return endpoint; }
    public void setEndpoint(String endpoint) { this.endpoint = endpoint; }

    public String getMethod() { return method; }
    public void setMethod(String method) { this.method = method; }

    public Map<String, Object> getExamplePayload() { return examplePayload; }
    public void setExamplePayload(Map<String, Object> examplePayload) {
        this.examplePayload = examplePayload;
    }

    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
}
