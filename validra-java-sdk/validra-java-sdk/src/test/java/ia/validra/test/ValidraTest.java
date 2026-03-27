package ia.validra.test;

import java.util.Map;

import org.testng.annotations.Test;

import ai.validra.Validra;
public class ValidraTest {

    @Test
    void ValidraBasicTestExample() {

        Validra.test()
                .endpoint("https://jsonplaceholder.typicode.com/posts")
                .method("POST")
                .examplePayload(Map.of(
                        "title", "foo",
                        "body", "bar",
                        "userId", 1
                ))
                .run();
    }
}
