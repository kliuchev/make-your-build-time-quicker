// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature04Data",
    products: [.library(name: "Feature04Data", targets: ["Feature04Data"])],
    dependencies: [.package(path: "../Feature04Domain")],
    targets: [.target(name: "Feature04Data", dependencies: [.product(name: "Feature04Domain", package: "Feature04Domain")])]
)
