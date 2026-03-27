package ai.validra;

import ai.validra.client.ValidraClient;
import ai.validra.model.TestRequest;

import java.util.Map;

public class Validra {

    private final TestRequest request = new TestRequest();

    public static Validra test() {
        return new Validra();
    }

    public Validra endpoint(String endpoint) {
        request.setEndpoint(endpoint);
        return this;
    }

    public Validra method(String method) {
        request.setMethod(method);
        return this;
    }

    public Validra examplePayload(Map<String, Object> payload) {
        request.setExamplePayload(payload);
        return this;
    }

    public void run() {
        ValidraClient.run(request);
    }
}
