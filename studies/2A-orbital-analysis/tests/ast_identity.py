"""Interpreter-neutral AST representation; exact source SHA remains primary."""
import ast,hashlib,json
def canonical_node(value):
 if isinstance(value,ast.AST):
  fields={}
  for name,child in ast.iter_fields(value):
   # Empty optional defaults differ in ast.dump formatting between Python versions.
   # Keep all nonempty fields, including False, 0, literal values and operations.
   if child is None or isinstance(child,list) and not child:continue
   fields[name]=canonical_node(child)
  return {"node":type(value).__name__,"fields":fields}
 if isinstance(value,list):return [canonical_node(x) for x in value]
 if value is Ellipsis:return {"constant":"Ellipsis"}
 return value
def stable_ast_sha256(node):
 return hashlib.sha256(json.dumps(canonical_node(node),sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()
