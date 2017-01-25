#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_previewer
----------------------------------

Tests for `previewer` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner
from py import path

from previewer import previewer
from previewer import cli


@pytest.fixture(autouse=True)
def initdir(tmpdir):
    fixture_basename = 'tests/assets'
    fixture_path = path.local(fixture_basename)
    fixture_path.copy(tmpdir / fixture_basename)
    tmpdir.chdir()  # change to pytest-provided temporary directory


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main, ['./tests/assets/room_4096.jpg'])
    assert result.exit_code == 0
    assert 'Image will be loaded from path' in result.output


def test_cli_preview_size(runner):
    result = runner.invoke(cli.main, ['--preview-height=630', '--preview-width=1120', './tests/assets/room_4096.jpg'])
    assert result.exit_code == 0
    assert "Preview will be generated at size '1120x630'" in result.output


def test_cli_fov(runner):
    result = runner.invoke(cli.main, ['--fov=80', './tests/assets/room_4096.jpg'])
    assert result.exit_code == 0
    assert "with fov = 80.0 degrees" in result.output


def test_cli_fov(runner):
    result = runner.invoke(cli.main, ['--latitude=10', '--longitude=20', './tests/assets/room_4096.jpg'])
    assert result.exit_code == 0
    assert "at (latitude, longitude) = (10.0, 20.0)" in result.output
