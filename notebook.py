import marimo

__generated_with = "0.9.17"
app = marimo.App()


@app.cell
def __(mo):
    mo.md("""#3D Geometry File Formats""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## About STL

        STL is a simple file format which describes 3D objects as a collection of triangles.
        The acronym STL stands for "Simple Triangle Language", "Standard Tesselation Language" or "STereoLitography"[^1].

        [^1]: STL was invented for – and is still widely used – for 3D printing.
        """
    )
    return


@app.cell
def __(mo, show):
    mo.show_code(show("data/teapot.stl", theta=45.0, phi=30.0, scale=2))
    return


@app.cell(hide_code=True)
def __(mo):
    with open("data/teapot.stl", mode="rt", encoding="utf-8") as _file:
        teapot_stl = _file.read()

    teapot_stl_excerpt = teapot_stl[:723] + "..." + teapot_stl[-366:]

    mo.md(
        f"""
    ## STL ASCII Format

    The `data/teapot.stl` file provides an example of the STL ASCII format. It is quite large (more than 60000 lines) and looks like that:
    """
    +
    f"""```
    {teapot_stl_excerpt}
    ```
    """
    +

    """
    """
    )
    return teapot_stl, teapot_stl_excerpt


@app.cell(hide_code=True)
def __(mo):
    mo.md(f"""

      - Study the [{mo.icon("mdi:wikipedia")} STL (file format)](https://en.wikipedia.org/wiki/STL_(file_format)) page (or other online references) to become familiar the format.

      - Create a STL ASCII file `"data/cube.stl"` that represents a cube of unit length  
        (💡 in the simplest version, you will need 12 different facets).

      - Display the result with the function `show` (make sure to check different angles).
    """)
    return


@app.cell
def __(mo, show):
    mo.show_code(show("data/cube.stl"))
    return


@app.cell
def __(mo):
    mo.md(r"""## STL & NumPy""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(rf"""

    ### NumPy to STL

    Implement the following function:

    ```python
    def make_STL(triangles, normals=None, name=""):
        pass # 🚧 TODO!
    ```

    #### Parameters

      - `triangles` is a NumPy array of shape `(n, 3, 3)` and data type `np.float32`,
         which represents a sequence of `n` triangles (`triangles[i, j, k]` represents 
         is the `k`th coordinate of the `j`th point of the `i`th triangle)

      - `normals` is a NumPy array of shape `(n, 3)` and data type `np.float32`;
         `normals[i]` represents the outer unit normal to the `i`th facet.
         If `normals` is not specified, it should be computed from `triangles` using the 
         [{mo.icon("mdi:wikipedia")} right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule).

      - `name` is the (optional) solid name embedded in the STL ASCII file.

    #### Returns

      - The STL ASCII description of the solid as a string.

    #### Example

    Given the two triangles that make up a flat square:

    ```python

    square_triangles = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            [[1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
        ],
        dtype=np.float32,
    )
    ```

    then printing `make_STL(square_triangles, name="square")` yields
    ```
    solid square
      facet normal 0.0 0.0 1.0
        outer loop
          vertex 0.0 0.0 0.0
          vertex 1.0 0.0 0.0
          vertex 0.0 1.0 0.0
        endloop
      endfacet
      facet normal 0.0 0.0 1.0
        outer loop
          vertex 1.0 1.0 0.0
          vertex 0.0 1.0 0.0
          vertex 1.0 0.0 0.0
        endloop
      endfacet
    endsolid square
    ```

    """)
    return


@app.cell
def __(np):
    def make_STL(triangles, normals=None, name=""):
        lines = []
        lines.append(f"solid {name}") #initialisation de la chaîne de caractères

        if normals is None: #calcul des normales si non spécifié, comme produit vectoriel normalisé
            vect1 = triangles[:, 1] - triangles[:, 0] #vecteur associé à un côté de chaque triangle
            vect2 = triangles[:, 2] - triangles[:, 0] #vecteur associé à un autre côté de chaque triangle
            normals = np.cross(vect1, vect2) #produit vectoriel des 2 vecteurs-côté
            norme = np.linalg.norm(normals, axis=1, keepdims=True) #calcul de la norme
            normals = normals/norme #normalisation (aucun vecteur n'est nul a priori, pas besoin de faire attention à ne pas diviser par 0)
        for normal, tri in zip(normals, triangles): #emploi de zip pour faire la boucle for en simultané sur normals et triangles
            lines.append(f"  facet normal {normal[0]} {normal[1]} {normal[2]}")
            lines.append("    outer loop")
            for vertex in tri:
                lines.append(f"      vertex {vertex[0]} {vertex[1]} {vertex[2]}")
            lines.append("    endloop")
            lines.append("  endfacet")
        lines.append(f"endsolid {name}")

        return "\n".join(lines) #ensemble des lignes jointes avec saut de ligne à chaque ligne
    return (make_STL,)


@app.cell
def __(make_STL, np):
    square_triangles = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            [[1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
        ],
        dtype=np.float32,
    )

    make_STL(square_triangles, name="square")
    return (square_triangles,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        ### STL to NumPy

        Implement a `tokenize` function


        ```python
        def tokenize(stl):
            pass # 🚧 TODO!
        ```

        that is consistent with the following documentation:


        #### Parameters

          - `stl`: a Python string that represents a STL ASCII model.

        #### Returns

          - `tokens`: a list of STL keywords (`solid`, `facet`, etc.) and `np.float32` numbers.

        #### Example

        For the ASCII representation the square `data/square.stl`, printing the tokens with

        ```python
        with open("data/square.stl", mode="rt", encoding="us-ascii") as square_file:
            square_stl = square_file.read()
        tokens = tokenize(square_stl)
        print(tokens)
        ```

        yields

        ```python
        ['solid', 'square', 'facet', 'normal', np.float32(0.0), np.float32(0.0), np.float32(1.0), 'outer', 'loop', 'vertex', np.float32(0.0), np.float32(0.0), np.float32(0.0), 'vertex', np.float32(1.0), np.float32(0.0), np.float32(0.0), 'vertex', np.float32(0.0), np.float32(1.0), np.float32(0.0), 'endloop', 'endfacet', 'facet', 'normal', np.float32(0.0), np.float32(0.0), np.float32(1.0), 'outer', 'loop', 'vertex', np.float32(1.0), np.float32(1.0), np.float32(0.0), 'vertex', np.float32(0.0), np.float32(1.0), np.float32(0.0), 'vertex', np.float32(1.0), np.float32(0.0), np.float32(0.0), 'endloop', 'endfacet', 'endsolid', 'square']
        ```
        """
    )
    return


@app.cell
def __(np):
    def tokenize(stl):
        tokens = []
        lines = stl.splitlines()
        for line in lines:
            elements = line.split()
            tokens.append(elements[0])
            if len(elements) > 1 and elements[1] == 'normal':
                tokens.append(elements[1])
                coord = [np.float32(x) for x in elements[2:]]
                tokens += coord
                continue
            if elements[0] == 'vertex':
                coord = [np.float32(x) for x in elements[1:]]
                tokens += coord
                continue
            tokens += elements[1:]
        return tokens

    with open("data/square.stl", mode="rt", encoding="us-ascii") as square_file:
        square_stl = square_file.read()
    tokens = tokenize(square_stl)
    tokens
    return square_file, square_stl, tokenize, tokens


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        Implement a `parse` function


        ```python
        def parse(tokens):
            pass # 🚧 TODO!
        ```

        that is consistent with the following documentation:


        #### Parameters

          - `tokens`: a list of tokens

        #### Returns

        A `triangles, normals, name` triple where

          - `triangles`: a `(n, 3, 3)` NumPy array with data type `np.float32`,

          - `normals`: a `(n, 3)` NumPy array with data type `np.float32`,

          - `name`: a Python string.

        #### Example

        For the ASCII representation `square_stl` of the square,
        tokenizing then parsing

        ```python
        with open("data/square.stl", mode="rt", encoding="us-ascii") as square_file:
            square_stl = square_file.read()
        tokens = tokenize(square_stl)
        triangles, normals, name = parse(tokens)
        print(repr(triangles))
        print(repr(normals))
        print(repr(name))
        ```

        yields

        ```python
        array([[[0., 0., 0.],
                [1., 0., 0.],
                [0., 1., 0.]],

               [[1., 1., 0.],
                [0., 1., 0.],
                [1., 0., 0.]]], dtype=float32)
        array([[0., 0., 1.],
               [0., 0., 1.]], dtype=float32)
        'square'
        ```
        """
    )
    return


@app.cell
def __(np, tokens):
    def parse(tokens):
        triangles = []
        normals = []
        name = ""
        i = 0 #compteur de mots
        while i < len(tokens): #boucle while plutôt que boucle for-python pour pouvoir sauter plusieurs indices d'un coup
            token = tokens[i] #on récupère le mot dans la liste
            if token == 'solid':
                i += 1
                while i < len(tokens) and tokens[i] != 'facet': #ajout du nom
                    name += tokens[i] + " "
                    i += 1
                name = name.strip() #on enlève les espaces inutiles
            elif token == 'facet' and tokens[i+1] == 'normal':
                normals.append([float(tokens[i+2]), float(tokens[i+3]), float(tokens[i+4])])
                i += 5        
            elif token == 'vertex':
                triangle = []
                for _ in range(3): #pas besoin de nom de variable de boucle
                    if tokens[i] == 'vertex':
                        triangle.append([float(tokens[i+1]), float(tokens[i+2]), float(tokens[i+3])])
                        i += 4
                triangles.append(triangle)
            elif token == 'endsolid': #fin de la description STL du solide
                break
            else:
                i += 1
        #conversion en tableaux numpy des listes triangles et normals
        triangles = np.array(triangles, dtype=np.float32)
        normals = np.array(normals, dtype=np.float32)
        return triangles, normals, name

    triangles, normals, name = parse(tokens)
    print(repr(triangles))
    print(repr(normals))
    print(repr(name))
    return name, normals, parse, triangles


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        rf"""
    ## Rules & Diagnostics



        Make diagnostic functions that check whether a STL model satisfies the following rules

          - **Positive octant rule.** All vertex coordinates are non-negative.

          - **Orientation rule.** All normals are (approximately) unit vectors and follow the [{mo.icon("mdi:wikipedia")} right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule).

          - **Shared edge rule.** Each triangle edge appears exactly twice.

          - **Ascending rule.** the z-coordinates of (the barycenter of) each triangle are a non-decreasing sequence.

    When the rule is broken, make sure to display some sensible quantitative measure of the violation (in %).

    For the record, the `data/teapot.STL` file:

      - 🔴 does not obey the positive octant rule,
      - 🟠 almost obeys the orientation rule, 
      - 🟢 obeys the shared edge rule,
      - 🔴 does not obey the ascending rule.

    Check that your `data/cube.stl` file does follow all these rules, or modify it accordingly!

    """
    )
    return


@app.cell
def __(np):
    def pos_octant_rule(triangles):
        vertices = triangles.size #nombre de sommets
        negative_vertices = np.sum(triangles < 0) #nombre de sommets négatifs
        percentage_neg = (negative_vertices/vertices)*100
        return {'rule': 'positive octant rule', 'number of violations': negative_vertices, 'percentage of violation': percentage_neg, 'rule satisfied': negative_vertices == 0}
    return (pos_octant_rule,)


@app.cell
def __(np):
    def orientation_rule(triangles, normals):
        #1ère vérification : normales = vecteurs unitaires ?
        norms = np.linalg.norm(normals, axis=1)
        pas_unitaires = np.sum(np.abs(norms - 1) > 1e-4) #nombre de normales non unitaires

        #2ème vérification : règle de la main droite ?
        vect1 = triangles[:, 1] - triangles[:, 0]
        vect2 = triangles[:, 2] - triangles[:, 0]
        prod_vect = np.cross(vect1, vect2)
        prod_vect /= np.linalg.norm(prod_vect, axis=1, keepdims=True)  #normalisation
        pas_rmd = np.sum(np.dot(prod_vect, normals.T).diagonal() < 0) #le nombre de normales ne suivant pas la règle de la main droite s'obtient par produit scalaire

        #pourcentage de violations
        total_triangles = triangles.shape[0]
        violation_percentage = ((pas_unitaires + pas_rmd) / total_triangles) * 100

        return {'rule': 'orientation rule', 'number of unitary violations': pas_unitaires, 'number of orientation violations': pas_rmd, 'percentage of violation': violation_percentage, 'rule satisfied': pas_unitaires == 0 and pas_rmd == 0}
    return (orientation_rule,)


@app.cell
def __():
    def shared_edge_rule(triangles):
        edges = []
        for triangle in triangles: #ajout des arêtes ordonnées (pour pouvoir les compter)
            edges.extend([(tuple(triangle[0]), tuple(triangle[1])), (tuple(triangle[1]), tuple(triangle[2])), (tuple(triangle[2]), tuple(triangle[0]))])
        sorted_edges = [tuple(sorted(edge)) for edge in edges] #on trie les arêtes pour éviter les doublons

        #occurrences des arêtes
        count_edges = {}
        for edge in sorted_edges:
            count_edges[edge] = count_edges.get(edge, 0) + 1 #on ajoute 1 au compte

        nb_edges = len(count_edges)
        violations = sum(1 for count in count_edges.values() if count != 2)
        violation_percentage = (violations / nb_edges) * 100

        return {'rule': 'shared edge rule', 'number of edges': nb_edges, 'number of violations': violations, 'percentage of violation': violation_percentage, 'satisfied': violations == 0}
    return (shared_edge_rule,)


@app.cell
def __(np):
    def ascending_rule(triangles):
        barycenters = np.mean(triangles, axis=1) #barycentres
        z_coord = barycenters[:, 2] #coordonnées selon z des barycentres
        violations = np.sum(np.diff(z_coord) < 0)
        violation_percentage = (violations/len(z_coord))*100

        return {'rule': 'ascending rule', 'number of triangles': len(barycenters), 'violations': violations, 'percentage of violations': violation_percentage, 'satisfied': violations == 0}
    return (ascending_rule,)


@app.cell
def __(parse, tokenize):
    with open("data/teapot.stl", mode="rt", encoding="us-ascii") as tea_file:
        tea_stl = tea_file.read()
    tokens_tea = tokenize(tea_stl)
    triangles_tea, normals_tea, name_tea = parse(tokens_tea)
    return (
        name_tea,
        normals_tea,
        tea_file,
        tea_stl,
        tokens_tea,
        triangles_tea,
    )


@app.cell
def __(pos_octant_rule, triangles_tea):
    pos_octant_rule(triangles_tea)
    return


@app.cell
def __(normals_tea, orientation_rule, triangles_tea):
    orientation_rule(triangles_tea, normals_tea)
    return


@app.cell
def __(shared_edge_rule, triangles_tea):
    shared_edge_rule(triangles_tea)
    return


@app.cell
def __(ascending_rule, triangles_tea):
    ascending_rule(triangles_tea)
    return


@app.cell
def __(parse, tokenize):
    with open("data/cube.stl", mode="rt", encoding="us-ascii") as cube_file:
        cube_stl = cube_file.read()
    tokens_cube = tokenize(cube_stl)
    triangles_cube, normals_cube, name_cube = parse(tokens_cube)
    return (
        cube_file,
        cube_stl,
        name_cube,
        normals_cube,
        tokens_cube,
        triangles_cube,
    )


@app.cell
def __(pos_octant_rule, triangles_cube):
    pos_octant_rule(triangles_cube)
    return


@app.cell
def __(normals_cube, orientation_rule, triangles_cube):
    orientation_rule(triangles_cube, normals_cube)
    return


@app.cell
def __(shared_edge_rule, triangles_cube):
    shared_edge_rule(triangles_cube)
    return


@app.cell
def __(ascending_rule, triangles_cube):
    ascending_rule(triangles_cube)
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""On voit que le fichier cube ne vérifie pas les règles suivantes : **positive octant** et **ascending**. On va donc devoir le modifier pour qu'il les vérifie.""")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""Pour la *positive octant rule*, on va regarder le sommet aux coordonnées "les plus négatives" et appliquer une translation d'ensemble pour avoir toutes les coordonnées positives.""")
    return


@app.cell
def __(np):
    def get_positive_octant(triangles):
        min_coords = np.min(triangles, axis=(0, 1)) #on trouve le triangle de coordonnées minimales
        translation = -np.min(min_coords, 0)
        new_triangles = triangles + translation
        return new_triangles
    return (get_positive_octant,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""Pour la *ascending rule*, on calcule les barycentres des triangles et on les range par z croissant.""")
    return


@app.cell
def __(np):
    def get_ascending(triangles):
        barycentres = np.mean(triangles, axis=1)
        sorted_indices = np.argsort(barycentres[:, 2])
        new_triangles = triangles[sorted_indices]
        return new_triangles
    return (get_ascending,)


@app.cell
def __(
    get_ascending,
    get_positive_octant,
    make_STL,
    mo,
    show,
    triangles_cube,
):
    #Nouveau cube respectant toutes les règles
    new_triangles = get_ascending(get_positive_octant(triangles_cube))
    stl_cube_corr = make_STL(new_triangles, name="corrected_cube")
    with open('data/corrected_cube.stl', mode='w', encoding='us-ascii') as stl_file:
        stl_file.write(stl_cube_corr)

    mo.show_code(show("data/corrected_cube.stl"))
    return new_triangles, stl_cube_corr, stl_file


@app.cell
def __(new_triangles, pos_octant_rule):
    pos_octant_rule(new_triangles)
    return


@app.cell
def __(ascending_rule, new_triangles):
    ascending_rule(new_triangles)
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
    rf"""
    ## OBJ Format

    The OBJ format is an alternative to the STL format that looks like this:

    ```
    # OBJ file format with ext .obj
    # vertex count = 2503
    # face count = 4968
    v -3.4101800e-003 1.3031957e-001 2.1754370e-002
    v -8.1719160e-002 1.5250145e-001 2.9656090e-002
    v -3.0543480e-002 1.2477885e-001 1.0983400e-003
    v -2.4901590e-002 1.1211138e-001 3.7560240e-002
    v -1.8405680e-002 1.7843055e-001 -2.4219580e-002
    ...
    f 2187 2188 2194
    f 2308 2315 2300
    f 2407 2375 2362
    f 2443 2420 2503
    f 2420 2411 2503
    ```

    This content is an excerpt from the `data/bunny.obj` file.

    """
    )
    return


@app.cell
def __(mo, show):
    mo.show_code(show("data/bunny.obj", scale="1.5"))
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        Study the specification of the OBJ format (search for suitable sources online),
        then develop a `OBJ_to_STL` function that is rich enough to convert the OBJ bunny file into a STL bunny file.
        """
    )
    return


@app.cell
def __(make_STL, np):
    def OBJ_to_STL(obj_path, stl_path):
        vertices = []
        triangles = []
        with open(obj_path, 'r') as obj_file:
            for line in obj_file:
                parts = line.split()
                if not parts:
                    continue
                if parts[0] == 'v':  #the line is a vertex
                    vertices.append(list(map(float, parts[1:4])))
                elif parts[0] == 'f':  #the line is a face
                    face = [int(idx.split('/')[0]) - 1 for idx in parts[1:4]] #conversion car la liste des vertices d'une face commence à 1 et pas à 0
                    triangle = [vertices[face[0]], vertices[face[1]], vertices[face[2]]]
                    triangles.append(triangle)

        triangles = np.array(triangles, dtype=np.float32)
        stl_description = make_STL(triangles, name='obj_to_stl')
        with open(stl_path, 'w') as stl_file:
            stl_file.write(stl_description)
    return (OBJ_to_STL,)


@app.cell
def __(OBJ_to_STL, mo, show):
    OBJ_to_STL('data/bunny.obj', 'data/bunny.stl')
    mo.show_code(show("data/bunny.stl"))
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        rf"""
    ## Binary STL

    Since the STL ASCII format can lead to very large files when there is a large number of facets, there is an alternate, binary version of the STL format which is more compact.

    Read about this variant online, then implement the function

    ```python
    def STL_binary_to_text(stl_filename_in, stl_filename_out):
        pass  # 🚧 TODO!
    ```

    that will convert a binary STL file to a ASCII STL file. Make sure that your function works with the binary `data/dragon.stl` file which is an example of STL binary format.

    💡 The `np.fromfile` function may come in handy.

        """
    )
    return


@app.cell
def __(mo, show):
    mo.show_code(show("data/dragon.stl", theta=75.0, phi=-20.0, scale=1.7))
    return


@app.cell
def __(make_STL, np):
    def STL_binary_to_text(stl_filename_in, stl_filename_out):
        with open(stl_filename_in, mode="rb") as file: #'rb' = lecture binaire
            _ = file.read(80) #on lit l'en-tête du fichier
            n = np.fromfile(file, dtype=np.uint32, count=1)[0] #nombre de triangles
            normals = []
            faces = []
            for i in range(n):
                normals.append(np.fromfile(file, dtype=np.float32, count=3)) #extraction de la normale (12 octets, soit 3 floats)
                faces.append(np.fromfile(file, dtype=np.float32, count=9).reshape(3, 3)) #extraction des coordonnées des sommets (36 octets, soit 9 floats)
                _ = file.read(2) #on ignore les octets d'attributs
        stl_text = make_STL(faces, normals)
        with open(stl_filename_out, mode="wt", encoding="utf-8") as file:
            file.write(stl_text)
    return (STL_binary_to_text,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(rf"""## Constructive Solid Geometry (CSG)

    Have a look at the documentation of [{mo.icon("mdi:github")}fogleman/sdf](https://github.com/fogleman/) and study the basics. At the very least, make sure that you understand what the code below does:
    """)
    return


@app.cell
def __(X, Y, Z, box, cylinder, mo, show, sphere):
    demo_csg = sphere(1) & box(1.5)
    _c = cylinder(0.5)
    demo_csg = demo_csg - (_c.orient(X) | _c.orient(Y) | _c.orient(Z))
    demo_csg.save('output/demo-csg.stl', step=0.05)
    mo.show_code(show("output/demo-csg.stl", theta=45.0, phi=45.0, scale=1.0))
    return (demo_csg,)


@app.cell(hide_code=True)
def __(mo):
    mo.md("""ℹ️ **Remark.** The same result can be achieved in a more procedural style, with:""")
    return


@app.cell
def __(
    box,
    cylinder,
    difference,
    intersection,
    mo,
    orient,
    show,
    sphere,
    union,
):
    demo_csg_alt = difference(
        intersection(
            sphere(1),
            box(1.5),
        ),
        union(
            orient(cylinder(0.5), [1.0, 0.0, 0.0]),
            orient(cylinder(0.5), [0.0, 1.0, 0.0]),
            orient(cylinder(0.5), [0.0, 0.0, 1.0]),
        ),
    )
    demo_csg_alt.save("output/demo-csg-alt.stl", step=0.05)
    mo.show_code(show("output/demo-csg-alt.stl", theta=45.0, phi=45.0, scale=1.0))
    return (demo_csg_alt,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        rf"""
    ## JupyterCAD

    [JupyterCAD](https://github.com/jupytercad/JupyterCAD) is an extension of the Jupyter lab for 3D geometry modeling.

      - Use it to create a JCAD model that correspond closely to the `output/demo_csg` model;
    save it as `data/demo_jcad.jcad`.

      - Study the format used to represent JupyterCAD files (💡 you can explore the contents of the previous file, but you may need to create some simpler models to begin with).

      - When you are ready, create a `jcad_to_stl` function that understand enough of the JupyterCAD format to convert `"data/demo_jcad.jcad"` into some corresponding STL file.
    (💡 do not tesselate the JupyterCAD model by yourself, instead use the `sdf` library!)


        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""Pour créer la fonction voulue, on doit d'abord rendre compte du fichier JCAD avec des objets de la librairie sdf. Ensuite, il faut pouvoir recréer l'objet avec sdf puis le convertir en STL.""")
    return


@app.cell
def __():
    with open('data/demo_jcad.jcad', mode='r') as f:
        lines = f.read()
    lines
    return f, lines


@app.cell
def __(json, np, sdf):
    def parse_jcad_sdf(fichier):
        with open(fichier, mode='r') as f:
            lines = json.load(f)
        shapes = {}
        res = 0
        for item in lines.get("objects"):
            shape_type = item.get("shape")
            if shape_type == "Part::Sphere":
                name = item.get("name")
                parameters = item.get("parameters")
                radius = parameters.get("Radius")
                shapes[name] = sdf.sphere(radius)
                shapes[res] = sdf.sphere(radius)
                res += 1
            elif shape_type == "Part::Box":
                name = item.get("name")
                parameters = item.get("parameters")
                dimensions = [parameters.get("Length"), parameters.get("Width"), parameters.get("Height")]
                shapes[name] = sdf.box(dimensions)
                shapes[res] = sdf.box(dimensions)
                res += 1
            elif shape_type == "Part::MultiCommon":
                name = item.get("name")
                param = item.get("dependencies")
                shapes[name] = sdf.intersection(shapes[param[0]], shapes[param[1]])
                shapes[res] = sdf.intersection(shapes[param[0]], shapes[param[1]])
                res += 1
            elif shape_type == "Part::Cylinder":
                name = item.get("name")
                parameters = item.get("parameters")
                height = parameters.get("Height")
                radius = parameters.get("Radius")
                cyl = sdf.cylinder(radius)
                placement = parameters.get("Placement")
                angle = placement.get("Angle")*(180/np.pi) #angle en radian pour sdf
                axis = placement.get("Axis")
                shapes[name] = sdf.rotate(cyl, angle, axis)
                shapes[res] = sdf.rotate(cyl, angle, axis)
                res += 1
            elif shape_type == "Part::Cut":
                name = item.get("name")
                param = item.get("dependencies")
                shapes[name] = sdf.difference(shapes[param[0]], shapes[param[1]])
                shapes[res] = sdf.difference(shapes[param[0]], shapes[param[1]])
                res += 1
        return shapes[res-1]
    return (parse_jcad_sdf,)


@app.cell
def __(parse_jcad_sdf):
    obj = parse_jcad_sdf('data/demo_jcad.jcad')
    return (obj,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""À ce stade, la fonction **parse_jcad_sdf** nous permettrait de récupérer le dernier objet SDF rentré dans le dictionnaire (objet final, donc) grâce à la variable itérante *res*. Reste à convertir cet objet SDF en STL.""")
    return


@app.cell
def __(obj):
    obj.save('data/demo_jcad.stl')
    return


@app.cell
def __():
    with open("data/demo_jcad.stl", mode="rt") as _file:
        demo_stl = _file.read()
    demo_stl
    return (demo_stl,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""*Je m'arrête ici pour ne pas y laisser ma santé mentale...*""")
    return


@app.cell
def __(mo):
    mo.md("""## Appendix""")
    return


@app.cell
def __(mo):
    mo.md("""### Dependencies""")
    return


@app.cell
def __():
    # Python Standard Library
    import json

    # Marimo
    import marimo as mo

    # Third-Party Librairies
    import numpy as np
    import matplotlib.pyplot as plt
    import mpl3d
    from mpl3d import glm
    from mpl3d.mesh import Mesh
    from mpl3d.camera import Camera

    import meshio

    np.seterr(over="ignore")  # 🩹 deal with a meshio false warning

    import sdf
    from sdf import sphere, box, cylinder
    from sdf import X, Y, Z
    from sdf import intersection, union, orient, difference

    mo.show_code()
    return (
        Camera,
        Mesh,
        X,
        Y,
        Z,
        box,
        cylinder,
        difference,
        glm,
        intersection,
        json,
        meshio,
        mo,
        mpl3d,
        np,
        orient,
        plt,
        sdf,
        sphere,
        union,
    )


@app.cell
def __(mo):
    mo.md(r"""### STL Viewer""")
    return


@app.cell
def __(Camera, Mesh, glm, meshio, mo, plt):
    def show(
        filename,
        theta=0.0,
        phi=0.0,
        scale=1.0,
        colormap="viridis",
        edgecolors=(0, 0, 0, 0.25),
        figsize=(6, 6),
    ):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1], xlim=[-1, +1], ylim=[-1, +1], aspect=1)
        ax.axis("off")
        camera = Camera("ortho", theta=theta, phi=phi, scale=scale)
        mesh = meshio.read(filename)
        vertices = glm.fit_unit_cube(mesh.points)
        faces = mesh.cells[0].data
        vertices = glm.fit_unit_cube(vertices)
        mesh = Mesh(
            ax,
            camera.transform,
            vertices,
            faces,
            cmap=plt.get_cmap(colormap),
            edgecolors=edgecolors,
        )
        return mo.center(fig)

    mo.show_code()
    return (show,)


@app.cell
def __(mo, show):
    mo.show_code(show("data/teapot.stl", theta=45.0, phi=30.0, scale=2))
    return


if __name__ == "__main__":
    app.run()
