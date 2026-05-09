package com.krischuang.applyflow.dto;

import com.krischuang.applyflow.entity.ApplicationStatus;
import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
public class JobApplicationRequest {

    @NotBlank(message = "Job title is required")
    private String jobTitle;

    @NotBlank(message = "Company name is required")
    private String companyName;

    private String jobUrl;
    private String location;
    private String salaryRange;
    private ApplicationStatus status;
    private String notes;
    private LocalDate appliedDate;
}
