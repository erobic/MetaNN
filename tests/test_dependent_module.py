import pytest
import sys
from copy import deepcopy

sys.path.append('../')

import torch
from torch import nn
from metann import DependentModule

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Flatten(nn.Module):
    def __init__(self):
        super(Flatten, self).__init__()

    def forward(self, x):
        return x.view(x.size(0), -1)


def test_dependent_module1():
    net = nn.Sequential(
        nn.Conv2d(3, 3, 3),
        nn.Conv2d(3, 3, 3),
        Flatten(),
        nn.Linear(3, 4),
    )
    net = DependentModule(net).to(device)
    x = torch.randn(3, 3, 5, 5).to(device)
    print(net)
    print("here")
    for p in net.dependents():
        print(f"dependent {p}")
    assert net(x).shape == torch.Size([3, 4])


def test_dependent_module():
    net = nn.Sequential(
        DependentModule(nn.Conv2d(3, 3, 3)),
        DependentModule(nn.Conv2d(3, 3, 3)),
        Flatten(),
        DependentModule(nn.Linear(3, 4)),
    )
    net = DependentModule(net).to(device)
    x = torch.randn(3, 3, 5, 5).to(device)
    for p in net.dependents():
        print(f"dependent {p}")
    assert net(x).shape == torch.Size([3, 4])


def test_deepcopy():
    net = nn.Sequential(
        nn.Conv2d(3, 3, 3),
        nn.Conv2d(3, 3, 3),
        Flatten(),
        nn.Linear(3, 4),
    )
    net = DependentModule(net).to(device)
    x = torch.randn(3, 3, 5, 5).to(device)
    net2 = deepcopy(net)
    print(net2)
    assert net2(x).shape == torch.Size([3, 4])


def test_resnet():
    try:
        from torchvision.models.resnet import resnet18
        from metann import Learner
        net = resnet18()
        net = Learner(net)
        print(net.functional(net.parameters(), True, torch.randn(3, 3, 224, 224)))
    except ImportError:
        Warning('torchvision not included, cannot be tested')
        return
    finally:
        return


if __name__ == "__main__":
    test_dependent_module()
