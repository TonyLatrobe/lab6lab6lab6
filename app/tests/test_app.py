from src.app import add

# install pytest
# >> sudo apt install python3-pytest
# >> cd ~/jenkins-terraform-k8s-secure/app
# >> pytest

def test_add():
    assert add(2, 3) == 5