import os, sys

# fonctions du programme
def usage():
	return "Simplement passer le numero du palet a faire sonner en parametre"


# point d'entree du programme
if len(sys.argv) > 1 :
	print sys.argv[1]
	print "execution du script..."
else:
	print usage()