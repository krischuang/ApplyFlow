package com.krischuang.applyflow.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI openAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("ApplyFlow API")
                        .description("AI-powered job application tracker. " +
                                "Track your job applications, manage statuses, " +
                                "and get AI-powered insights.")
                        .version("v1.0.0")
                        .contact(new Contact()
                                .name("Kris Chuang")
                                .email("kris.kh.chuang@gmail.com"))
                        .license(new License().name("MIT")))
                .servers(List.of(
                        new Server().url("http://localhost:8080").description("Local development")
                ));
    }
}
