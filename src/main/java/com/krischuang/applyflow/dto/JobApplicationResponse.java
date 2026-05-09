package com.krischuang.applyflow.dto;

import com.krischuang.applyflow.entity.ApplicationStatus;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Getter
@Builder
public class JobApplicationResponse {
    private Long id;
    private String jobTitle;
    private String companyName;
    private String jobUrl;
    private String location;
    private String salaryRange;
    private ApplicationStatus status;
    private String notes;
    private LocalDate appliedDate;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
