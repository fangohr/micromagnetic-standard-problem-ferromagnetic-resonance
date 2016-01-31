The mesh files here were created from the ``examesh`` mesh creation
utility that comes with Nmag.

The commands to create the mesh files were:
```
   ./examesh mesh.nmesh,120:24,120:24,5:2
   nmeshpp -c mesh.nmesh mesh_555.nmesh.h5
```
and
```
   ./examesh mesh.nmesh,120:60,120:60,5:5
   nmeshpp -c mesh.nmesh mesh_221.nmesh.h5
```


