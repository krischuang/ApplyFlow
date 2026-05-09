package com.krischuang.applyflow.service.impl;

import com.krischuang.applyflow.dto.JobApplicationRequest;
import com.krischuang.applyflow.dto.JobApplicationResponse;
import com.krischuang.applyflow.entity.ApplicationStatus;
import com.krischuang.applyflow.entity.JobApplication;
import com.krischuang.applyflow.exception.ResourceNotFoundException;
import com.krischuang.applyflow.repository.JobApplicationRepository;
import com.krischuang.applyflow.service.JobApplicationService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional
public class JobApplicationServiceImpl implements JobApplicationService {

    private final JobApplicationRepository repository;

    public JobApplicationServiceImpl(JobApplicationRepository repository) {
        this.repository = repository;
    }

    @Override
    public JobApplicationResponse create(JobApplicationRequest request) {
        JobApplication app = new JobApplication();
        mapRequestToEntity(request, app);
        if (app.getStatus() == null) {
            app.setStatus(ApplicationStatus.SAVED);
        }
        return toResponse(repository.save(app));
    }

    @Override
    @Transactional(readOnly = true)
    public List<JobApplicationResponse> findAll() {
        return repository.findAll().stream()
                .map(this::toResponse)
                .toList();
    }

    @Override
    @Transactional(readOnly = true)
    public JobApplicationResponse findById(Long id) {
        return toResponse(getOrThrow(id));
    }

    @Override
    public JobApplicationResponse update(Long id, JobApplicationRequest request) {
        JobApplication app = getOrThrow(id);
        mapRequestToEntity(request, app);
        return toResponse(repository.save(app));
    }

    @Override
    public void delete(Long id) {
        if (!repository.existsById(id)) {
            throw new ResourceNotFoundException("JobApplication not found with id: " + id);
        }
        repository.deleteById(id);
    }

    @Override
    public JobApplicationResponse updateStatus(Long id, ApplicationStatus status) {
        JobApplication app = getOrThrow(id);
        app.setStatus(status);
        return toResponse(repository.save(app));
    }

    private JobApplication getOrThrow(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("JobApplication not found with id: " + id));
    }

    private void mapRequestToEntity(JobApplicationRequest request, JobApplication app) {
        app.setJobTitle(request.getJobTitle());
        app.setCompanyName(request.getCompanyName());
        app.setJobUrl(request.getJobUrl());
        app.setLocation(request.getLocation());
        app.setSalaryRange(request.getSalaryRange());
        if (request.getStatus() != null) {
            app.setStatus(request.getStatus());
        }
        app.setNotes(request.getNotes());
        app.setAppliedDate(request.getAppliedDate());
    }

    private JobApplicationResponse toResponse(JobApplication app) {
        return JobApplicationResponse.builder()
                .id(app.getId())
                .jobTitle(app.getJobTitle())
                .companyName(app.getCompanyName())
                .jobUrl(app.getJobUrl())
                .location(app.getLocation())
                .salaryRange(app.getSalaryRange())
                .status(app.getStatus())
                .notes(app.getNotes())
                .appliedDate(app.getAppliedDate())
                .createdAt(app.getCreatedAt())
                .updatedAt(app.getUpdatedAt())
                .build();
    }
}
