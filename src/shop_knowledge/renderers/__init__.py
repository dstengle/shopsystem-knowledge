"""Renderers: client code that reads an artifact through the contract and gives back the files to publish, by path
under the directory asked for. A renderer writes nothing and changes nothing; the command line writes what it gives."""
from shop_knowledge.renderers import diagram, markdown, skill

RENDERERS = {"diagram": diagram.render, "markdown": markdown.render, "skill": skill.render}
