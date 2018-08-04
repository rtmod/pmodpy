def main():
    import argparse
    from usergraphs import user
    from pmodpy.src import moduluswalks
    parser = argparse.ArgumentParser(description='Allows for computing modulus of a graph from terminal commands')
    parser.add_argument("g", help="Name of graph as defined in usergraphs/user.py")
    parser.add_argument("object",help="walks, trees or general")
    parser.add_argument("--verbose", help="increase output verbosity",action="store_true")
    parser.add_argument("--file", help=" ",action="store_true")
    parser.add_argument("-o", "--output", default='results/output.csv', help="Directs the output to a name of your choice.")
    args=parser.parse_args()





    if args.object=="walks":
        
        g=eval('user.'+args.g+'()')
        from pmodpy.src import moduluswalks
        source = int(input('Source node: '))
        target=int(input('Target_node: '))
        p=int(input('Value of p: '))
        if args.verbose:
            final=moduluswalks.modulus_walks(p, g, source, target, eps=2e-36, verbose=1)
        else:
            final=moduluswalks.modulus_walks(p, g, source, target, eps=2e-36, verbose=0)
        filename=args.output

        import csv
        writer=csv.writer(open(filename,'w'))
        writer.writerow(map(str.strip,map(str,final[2])));
        writer.writerow(final[1]);
        writer.writerow([str(p)+"modulus = "+str(final[0])])
        
        






if __name__=="__main__":
    main()
