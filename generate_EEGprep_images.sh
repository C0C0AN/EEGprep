#Generate Dockerfile.

#!/bin/sh

 set -e

 # Generate Dockerfile.
generate_docker() {
  docker run --rm kaczmarj/neurodocker:0.5.0 generate docker \
             --base neurodebian:stretch-non-free \
             --pkg-manager apt \
             --freesurfer version=6.0.0 min=true \
             --miniconda \
                conda_install="python=3.6 numpy nipype nibabel pandas mne" \
                create_env='eegprep' \
                activate=true
}

generate_singularity() {
  docker run --rm kaczmarj/neurodocker:0.5.0 generate singularity \
            --base neurodebian:stretch-non-free \
            --pkg-manager apt \
            --freesurfer version=6.0.0 min=true \
            --install fsl-complete git num-utils gcc \
            --miniconda \
               conda_install="python=3.6 numpy nipype nibabel pandas mne" \
               create_env='eegprep' \
               activate=true 
}

# generate files
generate_docker > Dockerfile
generate_singularity > Singularity

# Build images using the saved files
#docker build -t eegprep:test .
#singularity build eegprep.simg Singularity
