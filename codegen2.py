#!/usr/bin/python
import os
import imp
import argparse
import jinja2

#Parse the arguments
parser = argparse.ArgumentParser(description='codegen2')
parser.add_argument('--workdir', required=True, help='Work directory name')
parser.add_argument('--model', required=True, help='Model file name relative to workdir')
args = parser.parse_args()

#Setup path and filenames
workdir_name = os.path.realpath(args.workdir)
model_filename = os.path.realpath(workdir_name+'/'+args.model)

#Load the model file as Python code
print("Loading model file: %s" % model_filename)
m = imp.load_source('model', model_filename)
#Check if the variable named generators exist
try:
	m.generators
except:
	print("ERROR: The model must define the 'generators' dictionary.")
	exit(1)
#Check if the variable named variables exist
try:
	m.variables
except:
	print("ERROR: The model must define the 'variables' dictionary.")
	exit(1)	

#Setup Jinja2 template engine
templateLoader = jinja2.FileSystemLoader( searchpath="/" )
templateEnv = jinja2.Environment( loader=templateLoader )

#Iterate through the templates and outputs
for template_name in m.generators.keys():
	#Prepare the file names
	template_filename = os.path.realpath(workdir_name+'/'+template_name)
	output_filename = os.path.realpath(workdir_name+'/'+m.generators[template_name])
	#Load the template
	print(">Loading template file: %s" % template_filename)
	template = templateEnv.get_template( template_filename )
	#Render the template
	print(">>Generating output: %s" % output_filename)
	output_text = template.render( m.variables )
	#Produce the output
	output = open(output_filename, 'w')
	output.write(output_text)
	output.close()

#End of processing
exit(0)