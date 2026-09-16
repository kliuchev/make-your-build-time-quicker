// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature24Data",
    products: [.library(name: "Feature24Data", targets: ["Feature24Data"])],
    dependencies: [.package(path: "../Feature24Domain")],
    targets: [.target(name: "Feature24Data", dependencies: [.product(name: "Feature24Domain", package: "Feature24Domain")])]
)
