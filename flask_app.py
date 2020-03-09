#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function
from flask import Flask,render_template,request
import importlib
import sys
import os
import json
from task_files import task_files

app=Flask(__name__)
app.secret_key=''
app.config['SESSION_TYPE']='filesystem'
config_file='config'
config=importlib.import_module(config_file)
function_names=config.functions
tasks=config.tasks
data_path='data.json'

#This is loading in all the the functions, So i can change these for my needs
path=os.path.dirname(os.path.realpath(__file__))
data_path=path+'/'+data_path
with open(path+'/'+'{0}_{1}_functions.json'.format(config.experiment,config.version)) as json_data: # I think these are the X values!
    functions=json.load(json_data)
    json_data.close()

#Load in the y values
with open(path+'/fun1.json') as f:
    train_fun1 = json.load(f)
    f.close()
training_trials = 1
experiements = 3
function_samples = {'fun1':train_fun1} #'pos_linear':train_lin, 'neg_quad':train_negquad, 'sinc_compressed':train_sinc}


with open(path+'/gradValues.json') as f: #add the rest in here
    grad_fun1 = json.load(f)
    f.close()

grads = {}
for i in range(0,4):
    grads[i] = grad_fun1[str(i)]


@app.route('/',methods=['GET','POST']) # Can change later!
def start():
    
    if "location" in request.args:
        return render_template(request.args["location"])
    
    data=request.get_json()
    if data!=None:
        with open(data_path) as json_data:
            all_data=json.load(json_data)
            json_data.close()
        all_data.append(data)
        with open(data_path,'w') as json_data:
            json.dump(all_data,json_data)
        return ''
        
    else:
        fi=int(request.args.get('fi'))
        ti=int(request.args.get('ti'))
        if 'sessionId' in request.args:
            somataSessionId = request.args.get('sessionId')
        else:
            somataSessionId = ''
        function_name=function_names[fi]
        goals=tasks[ti]
        functions = {}
        for i in range(experiements):
            functions[i+1] = function_samples[function_name][str(i+1)]
        #function=function_samples[function_name]#[training_trials]
        task=['start.html']+[a for b in [task_files[t] for t in goals] for a in b]+['last_page.html']
        
        all_args={
                 'somataSessionId':somataSessionId,
                 'training_trials':training_trials,
                 'function_samples':{i: function_samples[function_name][str(i)] for i in range(training_trials)},
                 'function':functions,
                 'grad': grads, #MAKE BETTER
                 'task':task,
                 'experiment':config.experiment,
                 'version':config.version,
                 'function_name':function_name,
                 'goals':goals,
                 'bar_height':config.bar_height,
                 'bar_width':config.bar_width,
                 'nbars':config.nbars,
                 'trials':config.trials,
                 'predict_trials':config.predict_trials,
                 'se_length':config.se_length,
                 'sinc_offset':config.sinc_offset,
                 'neg_quad_offset':config.neg_quad_offset,
                 'pos_quad_offset':config.pos_quad_offset
                 }
        
        return render_template('index.html',**all_args)
        
if __name__=="__main__":
    app.run()    
