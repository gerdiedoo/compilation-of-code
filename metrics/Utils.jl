using Pickle
using PyCall
using Statistics: mean
using Printf

py"""
import pickle
import numpy
 
def load_pickle(fpath):
    with open(fpath, "rb") as f:
        data = pickle.load(f)
    return data
"""

load_pickle = py"load_pickle"

function confusion(y :: Vector{Int}, ŷ :: Vector{Float32}, threshold)
    ŷ2 = ŷ .>= threshold
    TP = sum((y .== 1) .&& (ŷ2 .== 1))
    TN = sum((y .== 0) .&& (ŷ2 .== 0))
    FP = sum((y .== 0) .&& (ŷ2 .== 1))
    FN = sum((y .== 1) .&& (ŷ2 .== 0))
    Dict(:TP=>TP, :TN=>TN, :FP=>FP, :FN=>FN)
end

function sensitivity_specificity(conf)
    # True positives over all positives
    sensitivity = conf[:TP] / (conf[:TP] + conf[:FN])
    # True negatives over all negatives
    specificity = conf[:TN] / (conf[:TN] + conf[:FP])
    Dict(:sensitivity=>sensitivity, :specificity=>specificity)
end

function precision_recall(conf)
    # true positive over all predicted positives
    precision = conf[:TP] / (conf[:TP] + conf[:FP] + 1e-8)
    # same as sensitivity
    recall = conf[:TP] / (conf[:TP] + conf[:FN])
    Dict(:precision=>precision, :recall=>recall)
end

function f1(precision, recall)
    2 * (precision * recall) / (precision + recall + 1e-8)
end

function f1s(confs)
    precision(tp, fp) = tp / (tp + fp)
    recall(tp, fn) = tp / (tp + fn)
    
    
    prs = [precision_recall(conf) for conf ∈ confs]
    
    macro_precision = sum([pr[:precision] for pr ∈ prs]) / length(label_names)
    macro_recall = sum([pr[:recall] for pr ∈ prs]) / length(label_names)
    
    micro_recall = sum([conf[:TP] for conf ∈ confs]) / (sum([conf[:TP] for conf ∈ confs]) + sum([conf[:FN] for conf ∈ confs]))
    micro_precision = sum([conf[:TP] for conf ∈ confs]) / (sum([conf[:TP] for conf ∈ confs]) + sum([conf[:FP] for conf ∈ confs]) + 1e-8)
    
    Dict(:macro_precision  => macro_precision,
         :macro_recall     => macro_recall,
         :macro_f1         => f1(macro_precision, macro_recall),
         :micro_recall     => micro_recall,
         :micro_precision  => micro_precision,
         :micro_f1         => f1(micro_precision, micro_recall))
end

function other_metrics(y :: Matrix{Int}, ŷ :: Matrix{Float32}, threshold)
    ŷ = ŷ .>= threshold
    
    subset_acc = all(ŷ .== y, dims=1) |> mean
    hamming_loss = ŷ .⊻ y |> mean
    
    Dict(:subset_acc=>subset_acc, :hamming=>hamming_loss)
end
