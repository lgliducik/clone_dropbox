# coding: utf-8
from dropbox_clon_main import add_new_files

def test_empty():
    new_files, delete_files = add_new_files(
        current_content=set(),
        prev_content=set(),
        files_from_server=set())
    assert new_files == set()
    assert delete_files == set()

def test_new_files():
    new_files, delete_files = add_new_files(
        current_content={'1','2','3'},
        prev_content={'1','2'},
        files_from_server=set())
    assert new_files == {'3'}
    assert delete_files == set()

def test_delete_files():
    new_files, delete_files = add_new_files(
        current_content={'1','2'},
        prev_content={'1','2','3'},
        files_from_server=set())
    assert new_files == set()
    assert delete_files == {'3'}

def test_nothing_happing():
    new_files, delete_files = add_new_files(
        current_content={'1','2'},
        prev_content={'1','2'},
        files_from_server=set())
    assert new_files == set()
    assert delete_files == set()

def test_new_client():
    new_files, delete_files = add_new_files(
        current_content=set(),
        prev_content=set(),
        files_from_server={'1', '2'} )
    assert new_files == {'1', '2'}
    assert delete_files == set()

def test_delete_files():
    new_files, delete_files = add_new_files(
        current_content=set(),
        prev_content={'1','2'},
        files_from_server={'1', '2'} )
    assert new_files == set()
    assert delete_files == {'1','2'}