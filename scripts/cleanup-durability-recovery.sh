# clean up
# Delete read replica stack
aws cloudformation delete-stack-instances --stack-set-name rds-standby-durability-recovery --accounts '["000000000000"]' --regions us-east-2 --no-retain-stacks
# Delete read replica stack set
aws cloudformation delete-stack-set --stack-set-name rds-standby-durability-recovery

# Delete primary db stack
aws cloudformation delete-stack-instances --stack-set-name rds-active-durability-recovery --accounts '["000000000000"]' --regions '["us-east-1"]' --no-retain-stacks
# Delete primary db stack set
aws cloudformation delete-stack --region us-east-1 --stack-name rds-primary-durability-recovery

# Delete vpc db stacks
aws cloudformation delete-stack-instances --stack-set-name durability-recovery --accounts '["000000000000"]' --regions '["us-east-1","us-east-2"]' --no-retain-stacks
# Delete vpc db stack set
aws cloudformation delete-stack-set --stack-set-name durability-recovery