import { useEffect, useRef, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import * as d3 from "d3";

const NEON = {
  magenta: "#ff2bd6",
  cyan: "#22d3ee",
  green: "#4ade80",
  red: "#fb7185",
  orange: "#fb923c",
  blue: "#38bdf8",
  team: "#c084fc",
  company: "#7c3aed",
  unknown: "#64748b",
};

function nodeFill(n) {
  if (n.type === "team") return NEON.team;
  if (n.type === "company") return NEON.company;
  const r = n.relation_to_viewer || "unknown";
  if (r === "friend") return NEON.magenta;
  if (r === "colleague") return NEON.cyan;
  if (r === "manager") return NEON.orange;
  return NEON.unknown;
}

function edgeNeon(d) {
  if (d.edge_type === "review") return (d.weight || 0) >= 0 ? NEON.green : NEON.red;
  if (d.edge_type === "friend") return NEON.magenta;
  if (d.edge_type === "colleague") return NEON.cyan;
  if (d.edge_type === "manager") return NEON.orange;
  return NEON.blue;
}

export default function TrustGraph({ graphData, highlightNodeId, nameFilter = "" }) {
  const ref = useRef(null);
  const navigate = useNavigate();

  const { nodes: rawNodes, edges: rawEdges } = graphData || { nodes: [], edges: [] };

  const { nodes, links } = useMemo(() => {
    const nodesCopy = rawNodes.map((n) => ({ ...n }));
    const idSet = new Set(nodesCopy.map((n) => n.id));
    const linksClean = [];
    const seenE = new Set();
    for (const e of rawEdges) {
      if (idSet.has(e.from) && idSet.has(e.to)) {
        const sig = `${e.from}|${e.to}|${e.edge_type}|${e.weight}`;
        if (seenE.has(sig)) continue;
        seenE.add(sig);
        linksClean.push({ source: e.from, target: e.to, ...e });
      }
    }
    return { nodes: nodesCopy, links: linksClean };
  }, [rawNodes, rawEdges]);

  const filterLower = nameFilter.toLowerCase();

  useEffect(() => {
    const el = ref.current;
    if (!el || nodes.length === 0) return;

    const width = el.clientWidth || 800;
    const height = 420;
    el.innerHTML = "";

    const svg = d3.select(el).append("svg").attr("width", width).attr("height", height).attr("viewBox", [0, 0, width, height]);

    const defs = svg.append("defs");
    const filt = defs.append("filter").attr("id", "wt-neon-glow").attr("x", "-50%").attr("y", "-50%").attr("width", "200%").attr("height", "200%");
    filt.append("feGaussianBlur").attr("in", "SourceGraphic").attr("stdDeviation", 1.8).attr("result", "blur");
    const feMerge = filt.append("feMerge");
    feMerge.append("feMergeNode").attr("in", "blur");
    feMerge.append("feMergeNode").attr("in", "SourceGraphic");

    const gRoot = svg.append("g");
    const zoom = d3.zoom().scaleExtent([0.3, 4]).on("zoom", (ev) => gRoot.attr("transform", ev.transform));
    svg.call(zoom);

    const g = gRoot.append("g");

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d) => d.id)
          .distance(90)
      )
      .force("charge", d3.forceManyBody().strength(-240))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(30));

    const linkSel = g
      .append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke", (d) => edgeNeon(d))
      .attr("stroke-width", (d) => 1.5 + Math.min(4, Math.abs(d.weight || 0) * 2.5))
      .attr("stroke-dasharray", (d) => (d.edge_type === "review" ? "8 5" : "none"))
      .attr("stroke-linecap", "round")
      .attr("opacity", 0.95)
      .attr("filter", "url(#wt-neon-glow)");

    const nodeG = g
      .append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .style("cursor", "pointer")
      .on("click", (ev, d) => {
        ev.stopPropagation();
        if (d.type === "user") navigate(`/user/${d.id}`);
        else if (d.type === "team") navigate(`/team/${d.id}`);
        else if (d.type === "company") navigate(`/company/${d.id}`);
      });

    nodeG.each(function (d) {
      const base = d3.select(this);
      const label = d.label || d.id;
      const match =
        !filterLower ||
        label.toLowerCase().includes(filterLower) ||
        (d.id && d.id.toLowerCase().includes(filterLower));
      const dim = filterLower && !match ? 0.15 : 1;
      const isHi = highlightNodeId && d.id === highlightNodeId;
      const fill = nodeFill(d);

      if (d.type === "user") {
        base
          .append("circle")
          .attr("r", 18)
          .attr("fill", fill)
          .attr("opacity", dim)
          .attr("stroke", isHi ? NEON.cyan : "rgba(34,211,238,0.5)")
          .attr("stroke-width", isHi ? 3 : 1.5)
          .attr("filter", "url(#wt-neon-glow)");
      } else {
        const w = d.type === "company" ? 100 : 72;
        const h = 32;
        base
          .append("rect")
          .attr("x", -w / 2)
          .attr("y", -h / 2)
          .attr("width", w)
          .attr("height", h)
          .attr("rx", 8)
          .attr("fill", fill)
          .attr("opacity", dim)
          .attr("stroke", isHi ? NEON.magenta : "rgba(255,43,214,0.45)")
          .attr("stroke-width", isHi ? 3 : 1.5)
          .attr("filter", "url(#wt-neon-glow)");
      }

      base
        .append("text")
        .attr("text-anchor", "middle")
        .attr("dy", 4)
        .attr("font-size", 10)
        .attr("fill", "#e2e8f0")
        .attr("opacity", dim)
        .text((label || "").slice(0, 18));

      const title = `${label}${d.role ? ` — ${d.role}` : ""}`;
      base.append("title").text(title);
    });

    simulation.on("tick", () => {
      linkSel
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      nodeG.attr("transform", (d) => `translate(${d.x},${d.y})`);
    });

    return () => {
      simulation.stop();
    };
  }, [nodes, links, navigate, filterLower, highlightNodeId]);

  if (!rawNodes?.length) {
    return (
      <div
        className="wt-graph-shell"
        style={{
          height: 200,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "var(--bg-elevated)",
          borderRadius: "var(--radius)",
          border: "1px solid var(--border)",
          color: "var(--text-muted)",
        }}
      >
        No graph data
      </div>
    );
  }

  return (
    <div
      ref={ref}
      className="wt-graph-shell"
      style={{
        width: "100%",
        minHeight: 420,
        background: "linear-gradient(160deg, #050510 0%, #0a0a18 50%, #0f0820 100%)",
        borderRadius: "var(--radius)",
        border: "1px solid rgba(34, 211, 238, 0.15)",
        boxShadow: "var(--glow-cyan), inset 0 0 60px rgba(255, 43, 214, 0.04)",
        overflow: "hidden",
      }}
    />
  );
}
