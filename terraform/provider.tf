terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {

  project = "qwiklabs-gcp-01-22d8f72fa8b3"
  region  = "us-west1"
  zone    = "us-west1-b"
}

