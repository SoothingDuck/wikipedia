# -*- coding: utf-8 -*-

"""
wikipedia
---------

This module contains the classes used to represent and extract informations from wikipedia dumps

"""

__author__ = "Yvan Aillet"

import bz2
from lxml import etree

from wikipedia.etl.dump import Article
from abc import ABC, abstractmethod
import os
import csv
import json


class DumpExtractor(ABC):
    def __init__(self, dump):
        self._dump = dump

    @property
    def dump(self):
        return self._dump

    @abstractmethod
    def extract_nodes(self):
        pass

    @abstractmethod
    def extract_redirections(self):
        pass


class DumpFileExtractor(DumpExtractor):
    MEDIAWIKI_NS_VERSION = "{http://www.mediawiki.org/xml/export-0.11/}"

    def __init__(self, dump, directory_name):
        super().__init__(dump)
        self._directory_name = directory_name

    def __iter__(self):
        """
        Iterator function over wikipedia dump extracting articles

        :return: wikipedia Page object extracted in sequential order
        """
        # Selon qu'on est compressé ou non
        if ".bz2" in self.dump.filename:
            f = bz2.BZ2File(self.dump.filename, mode="r")
        else:
            f = open(self.dump.filename, "rb")

        for _, element in etree.iterparse(f, events=("end",)):
            if element.tag == "{}page".format(DumpFileExtractor.MEDIAWIKI_NS_VERSION):
                yield (Article(element, self.dump.lang))
            else:
                continue
            element.clear()

        f.close()

    def extract_nodes(self):
        # Nodes
        filename_path = os.path.join(
            self._directory_name, self.dump.node_filename)
        if not os.path.exists(filename_path):
            with open(filename_path, "w", newline="", encoding="utf-8") as jsonfile:
                for article in self:
                    if article.redirect_title is None:
                        json.dump({
                            "article_id": article.id,
                            "article_title": article.title.strip(),
                            "article_namespace": article.ns,
                            "article_text": article.text
                        }, jsonfile)
                        jsonfile.write("\n")

    def extract_redirections(self):
        # Redirections
        filename_path = os.path.join(
            self._directory_name, self.dump.redirection_filename
        )
        if not os.path.exists(filename_path):
            with open(filename_path, "w", newline="", encoding="utf-8") as jsonfile:
                for article in self:
                    if article.redirect_title is not None:
                        json.dump({
                            "article_id": article.id,
                            "article_title": article.title.strip(),
                            "redirection_title": article.redirect_title.strip()
                        }, jsonfile)
                        jsonfile.write("\n")

    def extract_links(self, maxlength_article_title=2000):
        # Links
        filename_path = os.path.join(
            self._directory_name, self.dump.link_filename)
        if not os.path.exists(filename_path):
            with open(filename_path, "w", newline="", encoding="utf-8") as jsonfile:
                for article in self:
                    if article.redirect_title is None:
                        if len(article.title.strip()) <= maxlength_article_title:
                            for link in article.links:
                                json.dump(
                                    {
                                        "article_id": article.id,
                                        "link_title": link.strip()
                                    }, jsonfile
                                )

    def extract_infoboxes(self):
        # Categories
        filename_path = os.path.join(
            self._directory_name, self.dump.infobox_filename)
        if not os.path.exists(filename_path):
            with open(filename_path, "w", newline="", encoding="utf-8") as jsonfile:
                for article in self:
                    if article.redirect_title is None:
                        for infobox in article.infoboxes:
                            json.dump({
                                "article_id": article.id,
                                "article_title": article.title.strip(),
                                "infobox": infobox.strip()
                            }, jsonfile)
                            jsonfile.write("\n")

    def extract_categories(self):
        # Categories
        filename_path = os.path.join(
            self._directory_name, self.dump.category_filename)
        if not os.path.exists(filename_path):
            with open(filename_path, "w", newline="", encoding="utf-8") as jsonfile:
                for article in self:
                    if article.redirect_title is None:
                        for category in article.categories:
                            json.dump({
                                "article_id": article.id,
                                "article_title": article.title.strip(),
                                "category": category.strip()
                            }, jsonfile)
                            jsonfile.write("\n")

    def extract_portals(self):
        # Portals
        filename_path = os.path.join(
            self._directory_name, self.dump.portal_filename)
        if not os.path.exists(filename_path):
            with open(filename_path, "w", newline="", encoding="utf-8") as jsonfile:
                for article in self:
                    if article.redirect_title is None:
                        for portal in article.portals:
                            json.dump({
                                "article_id": article.id,
                                "article_title": article.title.strip(),
                                "portal": portal.strip()
                            }, jsonfile)
                            jsonfile.write("\n")
