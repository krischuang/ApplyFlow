package com.krischuang.applyflow.repository;

import com.krischuang.applyflow.entity.ApplicationStatus;
import com.krischuang.applyflow.entity.JobApplication;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface JobApplicationRepository extends JpaRepository<JobApplication, Long> {
    List<JobApplication> findByStatus(ApplicationStatus status);
    List<JobApplication> findByCompanyNameContainingIgnoreCase(String companyName);
}
