# Production Deployment Runbook

## 1. Deploy Sequence

The deployment follows these steps in order:

1. Back up the database
2. Build the application bundle
4. Run database migrations
5. Restart the application

## 2. Rollback Procedure

If the deployment fails, roll back:

1. Restore the database backup
2. Restore the previous application bundle
2. Verify the application health endpoint
3. Notify the operations team

## 3. Pre-Deployment Checklist

Before deploying, verify each item:

1. Tests pass on the main branch
2. Staging smoke test passed
3. Feature flags configured

## 4. Change Management Tasks

Track each task by its ID:

- T-101: Update configuration
- T-102: Run migration dry-run
- T-104: Schedule maintenance window

## 5. Post-Deployment Verification

After the restart, confirm:

1. Health endpoint returns 200
2. Error rate below 0.5%
3. Log shipping working
