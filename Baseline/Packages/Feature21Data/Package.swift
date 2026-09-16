// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature21Data",
    products: [.library(name: "Feature21Data", targets: ["Feature21Data"])],
    dependencies: [.package(path: "../Feature21Domain")],
    targets: [.target(name: "Feature21Data", dependencies: [.product(name: "Feature21Domain", package: "Feature21Domain")])]
)
