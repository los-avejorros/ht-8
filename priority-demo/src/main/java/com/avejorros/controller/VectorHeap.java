package com.avejorros.controller;

import java.util.ArrayList;
import java.util.List;

import com.avejorros.interfaces.PriorityQueue;

public class VectorHeap<E extends Comparable<E>> implements PriorityQueue<E> {
  private List<E> heap;

  public VectorHeap() {
    heap = new ArrayList<>();
  }

  private void percolateUp(int index) {
    while (index > 0) {
      int parentIndex = (index - 1) / 2;
      if (heap.get(index).compareTo(heap.get(parentIndex)) >= 0)
        break;
      swap(index, parentIndex);
      index = parentIndex;
    }
  }

  private void percolateDown(int index) {
    int childIndex;
    while (true) {
      int leftChild = 2 * index + 1;
      int rightChild = 2 * index + 2;
      if (leftChild >= heap.size())
        break;

      childIndex = leftChild;
      if (rightChild < heap.size() && heap.get(rightChild).compareTo(heap.get(leftChild)) < 0) {
        childIndex = rightChild;
      }

      if (heap.get(index).compareTo(heap.get(childIndex)) <= 0)
        break;
      swap(index, childIndex);
      index = childIndex;
    }
  }

  private void swap(int i, int j) {
    E temp = heap.get(i);
    heap.set(i, heap.get(j));
    heap.set(j, temp);
  }

  @Override
  public void add(E element) {
    heap.add(element);
    percolateUp(heap.size() - 1);
  }

  @Override
  public E remove() {
    if (isEmpty())
      return null;
    E min = heap.get(0);
    heap.set(0, heap.get(heap.size() - 1));
    heap.remove(heap.size() - 1);
    if (!isEmpty())
      percolateDown(0);
    return min;
  }

  @Override
  public boolean isEmpty() {
    return heap.isEmpty();
  }

  @Override
  public int size() {
    return heap.size();
  }

  public E getFirst() {
    if (isEmpty())
      return null;
    return heap.get(0);
  }
}
