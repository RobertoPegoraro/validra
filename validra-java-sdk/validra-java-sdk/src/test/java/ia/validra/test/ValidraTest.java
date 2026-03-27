package ia.validra.test;

import ai.validra.Validra;

import org.testng.annotations.Test;

import java.util.Map;

public class ValidraTest {

    @Test
    void ValidraBasicTestExample() {

        Validra.test()
                .endpoint("https://jsonplaceholder.typicode.com/posts")
                .method("POST")
                .payload(Map.of(
                        "title", "foo",
                        "body", "bar",
                        "userId", 1
                ))
                .run();
    }
}
