#!/usr/bin/python3

import tensorflow as tf
import numpy as np
import timeit

import tf_G


def main():
  beta: float = 0.85

  edges_np: np.ndarray = tf_G.DataSets.naive_6()

  with tf.Session() as sess:
    writer: tf.summary.FileWriter = tf.summary.FileWriter(
      'logs/tensorflow/.')

    graph: tf_G.Graph = tf_G.GraphConstructor.from_edges(
      sess, "G1", edges_np, writer, is_sparse=False)

    pr: tf_G.PageRank = tf_G.AlgebraicPageRank(
      sess, "PR1", graph, beta)

    g_upgradeable: tf_G.Graph = tf_G.GraphConstructor.empty(
      sess, "G2", graph.n, writer)

    pr_upgradeable: tf_G.PageRank = tf_G.AlgebraicPageRank(
      sess, "PR2", g_upgradeable, beta)

    ranks: np.ndarray = pr.ranks_np()

    print(ranks)

    for e in edges_np:
      g_upgradeable.append(e[0], e[1])
      print("[" + str(e[0]) + ", " + str(e[1]) + "] added!")

    ranks_upgradeable: tf_G.PageRank = pr_upgradeable.ranks_np()
    print(ranks_upgradeable)

    writer.add_graph(sess.graph)


if __name__ == '__main__':
  main()
