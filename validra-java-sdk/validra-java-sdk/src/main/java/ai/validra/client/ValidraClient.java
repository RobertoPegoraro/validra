package ai.validra.client;

import ai.validra.model.TestRequest;
import io.restassured.RestAssured;

public class ValidraClient {

    private static final String BASE_URL = "http://localhost:8000"; //Fast API URL

    public static void run(TestRequest request) {

        var response = RestAssured.given()
                .baseUri(BASE_URL)
                .contentType("application/json")
                .body(request)
                .when()
                .post("/run");

        System.out.println(response.asPrettyString());
    }
}