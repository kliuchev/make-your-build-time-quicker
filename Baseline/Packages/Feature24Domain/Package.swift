// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature24Domain",
    products: [.library(name: "Feature24Domain", targets: ["Feature24Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature24Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
