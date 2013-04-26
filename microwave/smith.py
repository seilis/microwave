
import matplotlib as mpl
import matplotlib.pyplot as plt

def create_smith():
	# Create the figure object
	fig = plt.figure(facecolor='white')

	# Add a single plot to the figure
	ax = fig.add_subplot(1,1,1,aspect='equal')
	
	# Remove the figure boundaries
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	
	ax.spines['top'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.spines['right'].set_visible(False)

	# Add Smith-chart circles
	Circ_zero = plt.Circle((0,0),radius=1.0,linestyle='solid',linewidth=2,color='black',fill=False)
	Circ_unity = plt.Circle((0.5,0),radius=0.5,linestyle='solid',linewidth=1,color='grey',fill=False)
	Circ_imag_low = Arc((1,-1),2,2,angle=0.0,theta1=90.0,theta2=180.0,linestyle='solid',linewidth=1,color='grey',fill=False)
	Circ_imag_high = Arc((1,1),2,2,angle=0.0,theta1=180.0,theta2=270.0,linestyle='solid',linewidth=1,color='grey',fill=False)

	ax.axhline(0,xmin=-1,xmax=1,linestyle='solid',linewidth=1,color='grey')
	ax.add_patch(Circ_imag_high)
	ax.add_patch(Circ_imag_low)
	ax.add_patch(Circ_unity)
	ax.add_patch(Circ_zero)

	return fig
	
