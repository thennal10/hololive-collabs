<template>
  <div ref='root' class='network'>
  </div>
</template>

<script>
import { Network } from "vis-network/peer/esm/vis-network"
import { DataSet, DataView } from "vis-data/peer/esm/vis-data"
import collabs from "./../assets/collabs.json"

export default {
  name: 'NetworkContainer',
  props: {
    collabLimit: Number
  },
  data() {
    return {
      edgesView: '',
    }
  }
  ,
  mounted() {
    var nodes = new DataSet(collabs['nodes'].map(node => {
      node.color = this.getRandomColor()
      node.label = node.id
      return node
    }));

    var edges = new DataSet(collabs['edges'].map(edge => {
      edge.title = String(edge.value)
      return edge
    }));
    
    this.edgesView = new DataView(edges, { filter: this.edgesFilter })

    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: this.edgesView
    };
    var options = {
      'physics': {
        'barnesHut': {
          'springConstant': 0.01,
          'springLength': 500
          }
        },
      'nodes': {
        'shape': 'circularImage',
        'font': '14px arial white'
      },
      'edges': {
        'shadow': this.shadow
      }
      };

    // initialize your network!
    new Network(this.$refs.root, data, options);
  },
  watch: {
    collabLimit() {
      try {
        this.edgesView.refresh()
      }
      catch (error) {
        console.log(error)
      }
    }
  },
  methods: {
    edgesFilter(edge) {
      return edge.value > this.collabLimit
    },
    getRandomColor() {
      var letters = '0123456789ABCDEF';
      var color = '#';
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }
  }
}
</script>

<style scoped>
@import url('https://unpkg.com/vis-network/styles/vis-network.min.css');
.network {
  width: 100%;
  height: 100%;
  background-color: #222222;
}
</style>
