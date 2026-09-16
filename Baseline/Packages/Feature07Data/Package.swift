// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature07Data",
    products: [.library(name: "Feature07Data", targets: ["Feature07Data"])],
    dependencies: [.package(path: "../Feature07Domain")],
    targets: [.target(name: "Feature07Data", dependencies: [.product(name: "Feature07Domain", package: "Feature07Domain")])]
)
