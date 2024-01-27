ff = addfile("hflux_speedy_ver41.5_1979_2008_clim.t47.nc","r")

lshf = ff->lshf
sshf = ff->sshf


delete(lshf@_FillValue)
;delete(lshf@missing_value)

delete(sshf@_FillValue)
;delete(sshf@missing_value)


ofile = "hflux_speedy_ver41.5_1979_2008_clim.t47.grd"
setfileoption("bin","WriteByteOrder","BigEndian")

do i = 0, 12-1
lshf_i = lshf(i, :, :)
fbinrecwrite (ofile, -1, lshf_i)
end do

do i = 0, 12-1
sshf_i = sshf(i, :, :)
fbinrecwrite (ofile, -1, sshf_i)
end do

