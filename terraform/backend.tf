terraform {
  backend "local" {
    path = "terraform/state/terraform.tfstate"
  }
}

terraform {
  backend "gcs" {
    bucket  = "# REPLACE WITH YOUR BUCKET NAME"
    prefix  = "terraform/state"
  }
}

resource "google_storage_bucket" "test-bucket-for-state" {
  name        = "qwiklabs-gcp-03-c26136e27648"
  location    = "US"
  uniform_bucket_level_access = true
  force_destroy = true
}

## force_destroy = true argument to your google_storage_bucket resource. When you delete a bucket, this boolean option will delete all contained objects. I