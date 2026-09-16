// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature07Presentation",
    products: [.library(name: "Feature07Presentation", targets: ["Feature07Presentation"])],
    dependencies: [.package(path: "../Feature07Domain"),
        .package(path: "../Feature07Data")],
    targets: [.target(name: "Feature07Presentation", dependencies: [.product(name: "Feature07Domain", package: "Feature07Domain"), .product(name: "Feature07Data", package: "Feature07Data")])]
)
