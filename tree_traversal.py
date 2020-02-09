#!/usr/bin/env python
# -*- coding: utf-8 -*-

from queue import LifoQueue
import os
import boto3
from botocore.exceptions import ClientError
import logging

class Graph():

    def __init__(self, entry_point, bucket):
        self.vertices = {}
        self.entry_point = entry_point
        self.bucket = bucket

    def add_vertex(self, vertex):
        self.vertices[vertex] = set()

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)


    def dft(self, entry_path=None):
        if entry_path is None:
            entry_path = self.entry_point
            if os.path.isfile(self.entry_point):
                self.upload_file(entry_path, self.bucket, os.path.basename(entry_path))
                return True
        if os.path.isdir(entry_path):
            content = os.listdir(entry_path)
            split_point = self.entry_point.split("/")[-1]
        stack = LifoQueue()
        visited = set()
        for item in content:
            stack.put(item)

        while not stack.empty():
            node = stack.get()
            current_node = os.path.join(entry_path, node)
            if current_node not in visited:
                if os.path.isfile(current_node):
                    visited.add(current_node)
                    split = current_node.split(split_point)[1]
                    structure = f"{split_point}{split}"
                    connector = "#/"
                    connector = connector.join(structure.split("/"))
                    self.upload_file(current_node, self.bucket, connector)
                elif os.path.isdir(current_node):
                    self.dft(current_node)
                else:
                    print("Invalid")
                    return False

        return True

    def upload_file(self, file_name, bucket, object_name=None):
        if object_name is None:
            object_name = file_name

        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download_files(self):
        s3 = boto3.client('s3')
        results = s3.list_objects_v2(Bucket=self.bucket)
        contents = results.get("Contents")
        f = {} 
        root = None
        for i in contents:
            folders_files = (i.get('Key')).split("/")
            print(folders_files)
            test = self.create_tree(folders_files, f)
            
        root = list(f.keys())[0]
        self.traverse_download(f, s3, root)

    def create_tree(self, arr, result={}, previous=None):
        if len(arr) > 0:
            if previous is None and arr[0] not in result.keys():
                result[arr[0]] = set()
                self.create_tree(arr[1:], result, arr[0])
#
            if arr[0][-1] == "#" and arr[0] not in result.keys():
                result[previous].add(arr[0])
                result[arr[0]] = set()
                self.create_tree(arr[1:], result, arr[0])

            if arr[0][-1] == "#" and arr[0] in result.keys():
                self.create_tree(arr[1:], result, arr[0])

            if arr[0][-1] != "#" and len(arr) is 1 and previous:
                result[previous].add(arr[0])

            if arr[0][-1] != "#" and len(arr) is 1 and not previous:
                if arr[0] in result.keys():
                    result[arr[0]].add(arr[0])
                else:
                    result[arr[0]] = arr[0]

        return result
                

    def traverse_download(self, trans_obj, client, root, current_path=os.getcwd()):
        destination = current_path
        if root[-1] == "#":
            destination = os.path.join(current_path, root[:-1])
            if not os.path.exists(destination):
                os.makedirs(destination)

            for f in trans_obj[root]:
                self.traverse_download(trans_obj, client, f, current_path=destination)
        else:
            destination = current_path
            split = list(trans_obj.keys())[0][:-1]
            destination = destination.split(split)
            if len(destination) > 1:
                destination = (f"{split}{destination[1]}")
                destination = destination.split("/")
                pound = "#/"
                file_download = pound.join(destination)
                file_download = f"{file_download}#/{root}"
                client.download_file(self.bucket, file_download, f"{current_path}/{root}")
            else:
                client.download_file(self.bucket, root, f"{current_path}/{root}")



