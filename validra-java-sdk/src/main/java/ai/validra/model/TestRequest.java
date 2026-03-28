package ai.validra.model;

import java.util.Map;

public class TestRequest {

    private String endpoint;
    private String method;
    private Map<String, Object> payload;
    private String type = "fuzz";

    // getters & setters
    public String getEndpoint() { return endpoint; }
    public void setEndpoint(String endpoint) { this.endpoint = endpoint; }

    public String getMethod() { return method; }
    public void setMethod(String method) { this.method = method; }

    public Map<String, Object> getPayload() { return payload; }
    public void setPayload(Map<String, Object> payload) {
        this.payload = payload;
    }

    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
}
