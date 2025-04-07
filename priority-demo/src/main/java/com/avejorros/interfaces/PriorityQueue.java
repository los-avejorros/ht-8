package com.avejorros.interfaces;

public interface PriorityQueue<E extends Comparable<E>> {
  void add(E element);
  E remove();
  boolean isEmpty();
  int size();
}
