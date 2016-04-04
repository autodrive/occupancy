"""
mmgp, python gui tree walk, Jan 19 '13, http://stackoverflow.com/questions/14404982/python-gui-tree-walk

You can do it using the widget ttk.Treeview, there is a demo dirbrowser.py that does that. So all I can do here is
give a stripped version of it and explain how it works. First, here is the short version:

==========
It starts by listing the files and directories present in the path given by sys.argv[1]. You don't want to use os.walk
here as you show only the contents directly available in the given path, without going into deeper levels. The code
then proceeds to show such contents, and for directories it creates a dummy children so this Treeview entry will be
displayed as something that can be further expanded. Then, as you may notice, there is a binding to the virtual event
<<TreeviewOpen>> which is fired whenever the user clicks an item in the Treeview that can be further expanded (in this
case, the entries that represent directories). When the event is fired, the code ends up removing the dummy node that
was created earlier and now populates the node with the contents present in the specified directory. The rest of the
code is composed of details about storing additional info in the Treeview to make everything work.
"""

import os
import sys
import tkinter

# krawyoti and cfi, How do I check what version of Python is running my script?, Jul 7 '09,
#    http://stackoverflow.com/questions/1093322/how-do-i-check-what-version-of-python-is-running-my-script
if 3 > sys.version_info[0]:
    import ttk
else:
    # python 2.x ttk -> python 3.x tkinter.ttk
    import tkinter.ttk as ttk


def fill_tree(tree_view_local, node):
    if tree_view_local.set(node, "type") != 'directory':
        return

    path = tree_view_local.set(node, "fullpath")
    # Delete the possibly 'dummy' node present.
    tree_view_local.delete(*tree_view_local.get_children(node))

    # commented out unused local variable definition
    # parent = tree_view_local.parent(node)
    for p in os.listdir(path):
        p = os.path.join(path, p)
        p_type = None
        if os.path.isdir(p):
            p_type = 'directory'

        f_name = os.path.split(p)[1]
        oid = tree_view_local.insert(node, 'end', text=f_name, values=[p, p_type])
        if p_type == 'directory':
            tree_view_local.insert(oid, 0, text='dummy')


def update_tree(event):
    """
    handles virtual event '<<TreeviewOpen>>'
    fired whenever the user clicks an item in the Treeview that can be further expanded
    remove the dummy node that was created earlier and now populates the node with the contents present
    in the specified directory.
    mmgp, python gui tree walk, Jan 19 '13, http://stackoverflow.com/questions/14404982/python-gui-tree-walk

    :param event:
    :return:
    """
    tree_view_local = event.widget
    fill_tree(tree_view_local, tree_view_local.focus())


def create_root(tree_view_local, start_path):
    df_path = os.path.abspath(start_path)
    node = tree_view_local.insert('', 'end', text=df_path,
                                  values=[df_path, "directory"], open=True)
    fill_tree(tree_view_local, node)


def main():
    root = tkinter.Tk()

    tree_view = ttk.Treeview(columns=("fullpath", "type"), displaycolumns='')
    tree_view.pack(fill='both', expand=True)

    # if sys.argv is not given, use current folder as tree root
    start_path = os.curdir
    if 1 < len(sys.argv):
        start_path = sys.argv[1]

    create_root(tree_view, start_path)
    # binding to the virtual event
    # fired whenever the user clicks an item in the Treeview that can be further expanded
    # mmgp, python gui tree walk, Jan 19 '13, http://stackoverflow.com/questions/14404982/python-gui-tree-walk
    tree_view.bind('<<TreeviewOpen>>', update_tree)

    root.mainloop()


if __name__ == '__main__':
    main()
