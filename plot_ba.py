axisfont={'family':'Times New Roman',
     'style':'normal',
    'weight':'bold',
      'color':'black',
      'size':14}#轴标题

noticefont={'family':'Times New Roman',
     'style':'normal',
    'weight':'normal',
      'color':'black',
      'size':15}#注释

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
dir1="simdata//"
dir2="simpng//"
markers=["o","s","<","D"]
fig,ax1 = plt.subplots()
k=0
for i in [5,6,7]:
    simnetworkdict=np.load("simdata\\"+"ba_new_test_"+str(i)+".npz",allow_pickle=True)["recording"].item()
    lambda2=simnetworkdict["lambda2"]
    x=simnetworkdict["lambda1"]
    y=simnetworkdict['simz']
    ax1.plot(x,y,marker=markers[k],linestyle=":",color="black",mfc='cornflowerblue',markersize=8,label="$\\lambda_{\\Delta}$"+"="+str(lambda2))
    k+=1
ax1.set_xlabel("Rescaled Infectivity $\\lambda$ ",axisfont)
ax1.set_ylabel("$\\bar{\\rho}$",axisfont)
lgd = ax1.legend(fontsize=13, handlelength=1, handletextpad=0.3, borderaxespad=0.2,
                        loc='lower right', labelspacing=0.2, borderpad=0.4)
ax1.text(0.95,0.08,"SIS",noticefont)
ax1.add_artist(lgd)
ax1.spines['left'].set_color('black')
ax1.spines['bottom'].set_color('black')
#fig.legend(bbox_to_anchor=(0.26,0.85),frameon=False,markerscale=0.5,labelspacing=0,loc="upper center")
fig.show()


