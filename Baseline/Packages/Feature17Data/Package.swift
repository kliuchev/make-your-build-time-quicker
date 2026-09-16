// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature17Data",
    products: [.library(name: "Feature17Data", targets: ["Feature17Data"])],
    dependencies: [.package(path: "../Feature17Domain")],
    targets: [.target(name: "Feature17Data", dependencies: [.product(name: "Feature17Domain", package: "Feature17Domain")])]
)
