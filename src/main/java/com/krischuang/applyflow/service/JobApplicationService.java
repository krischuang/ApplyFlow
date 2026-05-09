package com.krischuang.applyflow.service;

import com.krischuang.applyflow.dto.JobApplicationRequest;
import com.krischuang.applyflow.dto.JobApplicationResponse;
import com.krischuang.applyflow.entity.ApplicationStatus;

import java.util.List;

public interface JobApplicationService {
    JobApplicationResponse create(JobApplicationRequest request);
    List<JobApplicationResponse> findAll();
    JobApplicationResponse findById(Long id);
    JobApplicationResponse update(Long id, JobApplicationRequest request);
    void delete(Long id);
    JobApplicationResponse updateStatus(Long id, ApplicationStatus status);
}
