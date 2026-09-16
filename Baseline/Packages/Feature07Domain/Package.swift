// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature07Domain",
    products: [.library(name: "Feature07Domain", targets: ["Feature07Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature07Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
