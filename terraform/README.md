# Terraform

### terraform taint to tell Terraform to recreate the instance:

```
terraform taint google_compute_instance.vm_instance
```

### Examine your state file:
```
terraform show
```

### migrate state
```
terraform init -migrate-state
```

### RECONFIGURE THE TERRAFORM STATE
```
terraform init -reconfigure
```

### refresh the state
```
terraform refresh
```