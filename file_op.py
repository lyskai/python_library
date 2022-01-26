



def compute_md5sum(file_name):
    cmd = "md5sum " + file_name
    res = sh(cmd)
    return(res.stdout.split()[0])
